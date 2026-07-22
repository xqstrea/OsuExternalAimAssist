import pyautogui
import keyboard


def scanner(x, y, circle_radius):
    black_threshold = 1
    color_threshold = 10

    while True:

        if keyboard.is_pressed('q'):
            print("scan stopped")
            return

        scan = pyautogui.pixel(x,y)
        if scan[0] + scan[1] + scan[2] <= black_threshold:
            print("NERO")
            while True:

                if keyboard.is_pressed('q'):
                    print("scan stopped")
                    return
                    
                scan = pyautogui.pixel(x,y)
                scanleft = pyautogui.pixel(int(x - circle_radius), y)
                scanright = pyautogui.pixel(int(x + circle_radius), y)

                #print(x,y)

                if ((scan[0] + scan[1] + scan[2] > color_threshold) or 
                   ((scanleft[0] + scanleft[1] + scanleft[2] > color_threshold) and 
                   (scanright[0] + scanright[1] + scanright[2] > color_threshold))): 

                    print("TROVATO")
                    return 
