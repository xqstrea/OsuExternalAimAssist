import pygetwindow
import os
import re
import time

def normalize(text):
    return re.sub(r'[^a-z0-9\s\[\]]', '', text.lower())

def getMapName():
    while True:
        activewin = pygetwindow.getActiveWindow()
        if activewin:
            if "osu!" in activewin.title and len(activewin.title) > 5:
                map_title = activewin.title
                map_title = map_title.replace("osu!  - ", "")
                map_title = map_title.replace("osu! - ", "")
                map_title = map_title.replace("Playing: ", "")

                map_title = map_title.strip()
                return map_title



def mapFolders(directory, map_name):
    folders = list()

    try:
        for entry in os.scandir(directory):
            if entry.is_dir():
                folderpath = os.path.join(directory, entry.name)

                try:
                    for subentry in os.scandir(folderpath):
                        if subentry.is_file() and normalize(map_name) in normalize(subentry.name):
                            folders.append(entry.name)
                            break

                except OSError as ex:
                    continue

    except Exception as ex:
        print(f"err : {ex}")    

    return folders


def getDiffName(map_name):
    diff = map_name.rpartition("[")[2] 
    diff = diff.rstrip("]")
    return f"[{diff}]"


def findMap(directory, diff_name):
    try:
        for entry in os.scandir(directory):
            if entry.is_file() and entry.name.endswith(".osu"):
                #print(entry.name)

                if normalize(diff_name) in normalize(entry.name):
                    filepath = os.path.join(directory, entry.name)

                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        
                    return content

        return None

    except Exception as ex:
        print(f"err: {ex}")
        return None



