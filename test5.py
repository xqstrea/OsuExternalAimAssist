"""
programma va solo per 1920 x 1080


PROBLEMI
- SE UNA MAPPA PARTE CON X ELEM NELLE STESSE COORDINATE, FA PIXEL SCAN SULL'ULTIMO ELEMENTO DI QUESTO STACK
        non è problema parser

        praticamente quando c'è uno stack, le note sono messe tutte sulle stesse coordinate ma in realtà solo l'ultima sarà
        alle sue "vere" coordinate

        pixel scan prima nota non va a buon fine in questo caso almeno che non si usa una skin con i cerchi pieni o numeri
        grandi almeno quanto è questo offset di posizione non calcolato dal file txt
        
        con i cerchi vuoti aka skin di rafis lo scan lo fa sul nulla, e continua a cercare non appena trova il primo cerchio che,
        o casualmente, oppure perchè è proprio l'ultimo dello stack, cade con il suo numero sul pixel che viene scansionato 

        offset probabilmente calcolabile trovando (se succede) le prime N note con stesse coordinate, e ricalcolando targetX targetY
        sommandoci N * stack_leniency in px

- spesso devo andare sulla console e cliccare q più volte per sbloccare lo script






PROBLEMI PIXEL SCANNING (teoricamente non fixabili perchè dipendono dal fatto che uso pixelscanning)
- problemi strani se la mappa è AR 0
        su alcune mappe come GREEN GREENS lo schermo non diventerà mai completamente nero perchè il primo cerchio comincia a comparire 
        mentre lo sfondo sta ancora diventando nero
        {{ Ho paura non si possa fixare }}

- C'è sempre bisogno di aggiungere un area centrale colorata di bianco al centro perfetto dello spinner (NELLA SKIN)

- se si passa con il cursore sopra la zona del primo cerchio il pixel scan non funzionerà:
            pre nero: pixelscan non trova mai schermo nero
            post nero, pre fade in: pixelscan vede il cursore e pensa che sia iniziata la mappa 







da fare:
- rendere l'avvio dell assist continuo e automatico (non far partire lo script ogni volta) [?]






non strettamente necessario:
- fare in modo che consideri anche le slider end / la durata degli slider:
        fixa il problema di quando mira troppo in fretta ad un cerchio vicino
        [SEMI FIXATO CON METODO ATTESA AR / 3]
"""

import mapfinder as mapFinder
import mapparser as mapParser
import mapoffsets as mapOffsets
import pixelscanner as pixelScanner
import modutils as modUtils
import config

import os
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import math

from pynput.keyboard import Key, Controller

import pygame
pygame.init()

audioCue = pygame.mixer.Sound("C:\\Users\\FiercePC\\Desktop\\python\\PROJECTS\\AIM_ASSIST_OSU\\ding.mp3")
audioCue.set_volume(0.1)

key = Controller()

pyautogui.PAUSE = 0
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.FAILSAFE = False

def move_smooth(target_x, target_y, circle_radius):
    with config.lock:
        strength = config.strength
        radius = config.radius  

    cur_x, cur_y = pyautogui.position()
    
    dx = target_x - cur_x
    dy = target_y -  cur_y
    distance = math.hypot(dx, dy) 

    if int(circle_radius - (circle_radius / 5)) < distance <= radius:
        nudge_x = dx * strength  
        nudge_y = dy * strength
        pyautogui.moveRel(nudge_x, nudge_y, _pause=False)


def main():
    songs_dir = "C:\\Users\\FiercePC\\AppData\\Local\\osu!\\Songs"
    map_finished: bool

    while True:

        print("Waiting for osu! window...")
        map_title = mapFinder.getMapName()
        
        try:
            if not map_title:
                print("No active osu! window detected.")
                continue
            print(f"Detected osu! window: {map_title}")
            print("Cleaned map title:", map_title)
        except Exception as e:
            print(f"Error detecting map title: {e}")
            time.sleep(1)
            continue

        try:
            diff_name = mapFinder.getDiffName(map_title)
            if not diff_name:   
                print("Failed to extract difficulty from windo w title.")
                continue
            print(f"Extracted difficulty: {diff_name}")
        except Exception as e:
            print(f"Error extracting difficulty: {e}")
            time.sleep(1)
            continue

        try:
            if not os.path.exists(songs_dir):
                print(f"Songs directory not found: {songs_dir}")
                continue
        except Exception as e:
            print(f"Error checking songs directory: {e}")
            time.sleep(1)
            continue

        print("Searching for map name:", map_title.split(" [")[0])

        try:
            folders = mapFinder.mapFolders(songs_dir, map_title.split(" [")[0])
            if not folders:
                print("No folders found containing this map.")
                continue
            print(f"Found map in folders: {folders}")
        except Exception as e:
            print(f"Error finding map folders: {e}")
            time.sleep(1)
            continue

        try:
            osu_content = None
            for x in range(0, len(folders)):
                folder_path = os.path.join(songs_dir, folders[x])
                osu_content = mapFinder.findMap(folder_path, diff_name)
                if osu_content:
                    print(f".osu file content successfully loaded from {folders[x]}.\n")
                    break
                else: 
                    print(f"Failed to find .osu file with difficulty '{diff_name}' in folder {folders[x]}.")
            if not osu_content:
                print("Could not load .osu file from any folder.")
                continue
        except Exception as e:
            print(f"Error loading .osu file: {e}")
            time.sleep(1)
            continue

        hits = mapParser.parse_hitobjects(osu_content)
        stats = mapParser.parse_stats(osu_content)
        timing_points = mapParser.parse_timingPoints(osu_content)


        """
        for tp in timing_points:
            if tp["is_bpm"] == 1:
                bpm = 60000 / tp["beat_length"] 
                print(f"BPM {bpm:.2f} at {tp['offset']} ms")
            else:
                sv = 100 / abs(tp["beat_length"])
                print(f"Slider velocity {sv:.2f} at {tp['offset']} ms")
        """


        AR = float(stats["ApproachRate"])
        CS = float(stats["CircleSize"])
        slider_multiplier = float(stats["SliderMultiplier"])

        circle_radius = modUtils.csRadiusToPX(CS)
        print(circle_radius)

        print()
        print(slider_multiplier)

        with config.lock:
            speed = config.speed_mod
            mod = config.diff_mod

        if mod == "HR":
            AR = modUtils.ARHR(AR)
            CS = modUtils.csToHR(CS)
            modUtils.hrPos(hits)

        elif mod == "EZ":
            AR = modUtils.AREZ(AR)
            CS = modUtils.csToEZ(CS)


        if speed == "DT":
            AR = modUtils.ARDT(AR)
        elif speed == "HT":
            AR = modUtils.ARHT(AR)


        print(AR)
        arMS = modUtils.arToMS(AR)
        print(arMS)
    
        new_offset = mapOffsets.offsets(hits, speed, arMS)

        firstX = hits[0]["x"]
        firstY = hits[0]["y"]

        print(hits[0]["time"])

        print("")
        print(new_offset[0])
        print(firstX, firstY)
        print("")

        pixelScanner.scanner(firstX, firstY, circle_radius)

        audioCue.play()
        start_time = time.time()
        print(map_title)
        

        for i in range(0, len(hits)):
            if keyboard.is_pressed("q"):
                break

            target_x = hits[i]["x"] 
            target_y = hits[i]["y"]
            
            target_arrival_time = (new_offset[i]) / 1000.0

            while (time.time() - start_time) < target_arrival_time: 
                if keyboard.is_pressed("q"):
                    break

                if (time.time() - start_time) - target_arrival_time > (-1 * (arMS / 1000)) / 3 and (not (hits[i]["obj_type"] & 8)):
                    move_smooth(target_x, target_y, circle_radius)

                else:
                    pass

                time.sleep(0.002)

if __name__ == '__main__':
    main()
