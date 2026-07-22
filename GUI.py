import config

import dearpygui.dearpygui as gui
import win32gui
import win32con
import win32api

def on_auto_change(sender, app_data):
    with config.lock:
        if app_data:
            prev_radius = config.radius
            config.radius = 2000
        else:
            config.radius = getattr(config, "radius", config.radius)

def on_radius_change(sender, app_data):
    with config.lock:
        config.radius = app_data

def on_force_change(sender, app_data):
    with config.lock:
        config.strength = app_data

def on_speed_change(sender, app_data):
    with config.lock:
        config.speed_mod = app_data

def on_mod_change(sender, app_data):
    with config.lock:
        config.diff_mod = app_data

def main():

    gui.create_context()
    CHROMA_RGB = (255, 0, 255)
    

    with gui.window(label="Aim Assist", 
                    width=600, 
                    height=450, 
                    pos=(0, 0), 
                    no_close=True,
                    no_collapse=True,
                    no_resize=True
                    ):

        gui.add_text("External pixel scan aim assist")    
        
        gui.add_spacer(height=10)
        gui.add_separator()
        gui.add_spacer(height=10)

        with gui.group():
            gui.add_slider_int(label="Radius", 
                               default_value=50, 
                               max_value=500, 
                               callback=on_radius_change)

            gui.add_slider_float(label="Force", 
                                 default_value=0.01, 
                                 max_value=0.2, 
                                 format="%.2f",
                                 callback=on_force_change)

            gui.add_checkbox(label="Autopilot",
                             callback=on_auto_change)

        gui.add_spacer(height=10)
        gui.add_separator()
        gui.add_spacer(height=10)


        with gui.group():
            gui.add_radio_button(label="Speed variations:", 
                                 items=["NM", "DT", "HT"], 
                                 default_value="NM", 
                                 callback=on_speed_change, 
                                 tag="speed_radio",
                                 horizontal=True)

            gui.add_radio_button(label="Mods:", 
                                 items=["NM", "HR", "EZ"], 
                                 default_value="NM", 
                                 callback=on_mod_change, 
                                 tag="mod_radio", 
                                 horizontal=True)

        gui.add_spacer(height=10)   
        gui.add_separator()
        gui.add_spacer(height=10)

        gui.add_text("Click 'Q' to stop the aim assist") 
        



    with gui.theme() as global_theme:
        with gui.theme_component(gui.mvAll):

            gui.add_theme_color(gui.mvThemeCol_WindowBg, (51, 30, 56))
            gui.add_theme_color(gui.mvThemeCol_TitleBg, (51, 30, 56))
            gui.add_theme_color(gui.mvThemeCol_TitleBgActive, (112, 105, 147))

            gui.add_theme_style(gui.mvStyleVar_FrameRounding, 6)
            gui.add_theme_style(gui.mvStyleVar_WindowRounding, 6)
            gui.add_theme_style(gui.mvStyleVar_FramePadding, 6, 4)

        with gui.theme_component(gui.mvButton):
            gui.add_theme_color(gui.mvThemeCol_Button, (112, 160, 175))
            gui.add_theme_color(gui.mvThemeCol_ButtonHovered, (112, 160, 175))
            gui.add_theme_color(gui.mvThemeCol_ButtonActive, (112, 160, 175))


    with gui.font_registry():
        default_font = gui.add_font("C:/Windows/Fonts/Verdana.ttf", 18)

    gui.bind_theme(global_theme)
    gui.bind_font(default_font)


    gui.create_viewport(title="osu Aim Assist", width=1920, height=1080, decorated=False)
    gui.set_viewport_clear_color((*CHROMA_RGB, 255))
    gui.setup_dearpygui()
    gui.show_viewport()



    hwnd = win32gui.FindWindow(None, "osu Aim Assist")

    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                           ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST)

    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*CHROMA_RGB), 0, win32con.LWA_COLORKEY)

    gui.start_dearpygui()
    gui.destroy_context()

if __name__ == '__main__':
    main()  