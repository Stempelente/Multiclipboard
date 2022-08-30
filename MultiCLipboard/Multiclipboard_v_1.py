from optparse import Values
from unittest.loader import VALID_MODULE_NAME
import PySimpleGUI as sg
import pyperclip as pc
import keyboard as kb
import textwrap
from pynput.keyboard import Key, Controller

keyboard = Controller()

global BButton

sg.theme("DefaultNoMoreNagging")

def fadeaway():
    USE_FADE_IN = True
    WIN_MARGIN = 60

    # colors
    WIN_COLOR = "#282828"
    TEXT_COLOR = "#ffffff"

    DEFAULT_DISPLAY_DURATION_IN_MILLISECONDS = 300

    # Base64 Images to use as icons in the window
    img_error = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAA3NCSVQICAjb4U/gAAAACXBIWXMAAADlAAAA5QGP5Zs8AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAIpQTFRF////20lt30Bg30pg4FJc409g4FBe4E9f4U9f4U9g4U9f4E9g31Bf4E9f4E9f4E9f4E9f4E9f4FFh4Vdm4lhn42Bv5GNx5W575nJ/6HqH6HyI6YCM6YGM6YGN6oaR8Kev9MPI9cbM9snO9s3R+Nfb+dzg+d/i++vt/O7v/fb3/vj5//z8//7+////KofnuQAAABF0Uk5TAAcIGBktSYSXmMHI2uPy8/XVqDFbAAAA8UlEQVQ4y4VT15LCMBBTQkgPYem9d9D//x4P2I7vILN68kj2WtsAhyDO8rKuyzyLA3wjSnvi0Eujf3KY9OUP+kno651CvlB0Gr1byQ9UXff+py5SmRhhIS0oPj4SaUUCAJHxP9+tLb/ezU0uEYDUsCc+l5/T8smTIVMgsPXZkvepiMj0Tm5txQLENu7gSF7HIuMreRxYNkbmHI0u5Hk4PJOXkSMz5I3nyY08HMjbpOFylF5WswdJPmYeVaL28968yNfGZ2r9gvqFalJNUy2UWmq1Wa7di/3Kxl3tF1671YHRR04dWn3s9cXRV09f3vb1fwPD7z9j1WgeRgAAAABJRU5ErkJggg=='
    img_success = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAA3NCSVQICAjb4U/gAAAACXBIWXMAAAEKAAABCgEWpLzLAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAHJQTFRF////ZsxmbbZJYL9gZrtVar9VZsJcbMRYaMZVasFYaL9XbMFbasRZaMFZacRXa8NYasFaasJaasFZasJaasNZasNYasJYasJZasJZasJZasJZasJZasJYasJZasJZasJZasJZasJaasJZasJZasJZasJZ2IAizQAAACV0Uk5TAAUHCA8YGRobHSwtPEJJUVtghJeYrbDByNjZ2tvj6vLz9fb3/CyrN0oAAADnSURBVDjLjZPbWoUgFIQnbNPBIgNKiwwo5v1fsQvMvUXI5oqPf4DFOgCrhLKjC8GNVgnsJY3nKm9kgTsduVHU3SU/TdxpOp15P7OiuV/PVzk5L3d0ExuachyaTWkAkLFtiBKAqZHPh/yuAYSv8R7XE0l6AVXnwBNJUsE2+GMOzWL8k3OEW7a/q5wOIS9e7t5qnGExvF5Bvlc4w/LEM4Abt+d0S5BpAHD7seMcf7+ZHfclp10TlYZc2y2nOqc6OwruxUWx0rDjNJtyp6HkUW4bJn0VWdf/a7nDpj1u++PBOR694+Ftj/8PKNdnDLn/V8YAAAAASUVORK5CYII='

    # -------------------------------------------------------------------

    def display_notification(title, message, icon, display_duration_in_ms=DEFAULT_DISPLAY_DURATION_IN_MILLISECONDS, use_fade_in=True, alpha=0.9, location=None):

        # Compute location and size of the window
        message = textwrap.fill(message, 50)
        win_msg_lines = message.count("\n") + 1

        screen_res_x, screen_res_y = sg.Window.get_screen_size()
        win_margin = WIN_MARGIN  # distance from screen edges
        win_width, win_height = 364, 66 + (14.8 * win_msg_lines)
        win_location = location if location is not None else (screen_res_x - win_width - win_margin, screen_res_y - win_height - win_margin)

        layout = [[sg.Graph(canvas_size=(win_width, win_height), graph_bottom_left=(0, win_height), graph_top_right=(win_width, 0), key="-GRAPH-",
                            background_color=WIN_COLOR, enable_events=True)]]

        window = sg.Window(title, layout, background_color=WIN_COLOR, no_titlebar=True,
                        location=win_location, keep_on_top=True, alpha_channel=0, margins=(0, 0), element_padding=(0, 0),
                        finalize=True)

        window["-GRAPH-"].draw_rectangle((win_width, win_height), (-win_width, -win_height), fill_color=WIN_COLOR, line_color=WIN_COLOR)
        window["-GRAPH-"].draw_image(data=icon, location=(20, 20))
        window["-GRAPH-"].draw_text(title, location=(64, 20), color=TEXT_COLOR, font=("Arial", 12, "bold"), text_location=sg.TEXT_LOCATION_TOP_LEFT)
        window["-GRAPH-"].draw_text(message, location=(64, 44), color=TEXT_COLOR, font=("Arial", 9), text_location=sg.TEXT_LOCATION_TOP_LEFT)

        # change the cursor into a "hand" when hovering over the window to give user hint that clicking does something
        window['-GRAPH-'].set_cursor('hand2')

        if use_fade_in == True:
            for i in range(1,int(alpha*100)):               # fade in
                window.set_alpha(i/100)
                event, values = window.read(timeout=1)
                if event != sg.TIMEOUT_KEY:
                    window.set_alpha(1)
                    break
            event, values = window(timeout=display_duration_in_ms)
            if event == sg.TIMEOUT_KEY:
                for i in range(int(alpha*100),1,-1):       # fade out
                    window.set_alpha(i/100)
                    event, values = window.read(timeout=1)
                    if event != sg.TIMEOUT_KEY:
                        break
        else:
            window.set_alpha(alpha)
            event, values = window(timeout=display_duration_in_ms)

        window.close()

    if __name__ == '__main__':
        title = "Multiclipduck"
        message = c 
        display_notification(title, message, img_success, 100, use_fade_in=True)

def ende():
    ende_layout = [[sg.Text("Danke fürs Benutzen meiner kleinen App")],
                    [sg.Button("Beenden")]
                    ]

    ende_window = sg.Window("Ende im Gelände", ende_layout)

    while True:
        event, values = ende_window.read()

        if event == sg.WIN_CLOSED:
            break
        if event == "Beenden":
            break

def mcd(ersterhotkey, zweiterhotkey, BButton):

    mcd_layout = [[sg.Text("Speicher für: " + ersterhotkey), sg.InputText()]
                ]

    if BButton == True:
        mcd_layout.append([sg.Text("Speicher für " + zweiterhotkey), sg.InputText()]) 
    
    mcd_layout.append([sg.Push(),sg.Button("Neue Hotkeys belegen"),sg.Button("Beenden"), sg.Push()])

    mcd_window = sg.Window("Multiclipboard", mcd_layout)

    while True:
        event, values = mcd_window.read(timeout=100)
        if event == "Beenden" or sg.WIN_CLOSED:
            ende()
            break
        if event == "Neue Hotkeys belegen":
            mcd_window.close()
            greetw()
        if not values[0] == "":
            if BButton == True:
                if kb.is_pressed(zweiterhotkey):
                    global c
                    if values[1] == "":
                        c = "Keine Daten vorhanden"
                        fadeaway()
                    else:
                        pc.copy(values[1])
                        c = "Es wurde \"" + values[1] + "\" in den Cache geladen."
                        fadeaway()                        

            if kb.is_pressed(ersterhotkey):
                pc.copy(values[0])
                c = values[0]
                c = "Es wurde \"" + values[0] + "\" in den Cache geladen."
                fadeaway()

def zweiterButtonP(ersterhotkey, zweiterhotkey, BButton):
    zweiterButtonP_layout = [[sg.Text("Du hast " + zweiterhotkey + " gedrückt! Stimmt das?")],
                        [sg.Push(), sg.Button("Ja"), sg.Button("Nein"),sg.Push()]
    ]
    zweiterButtonP_window = sg.Window("Multiclipboardduck", zweiterButtonP_layout)

    while True:
        event, values = zweiterButtonP_window.read()
        if event == "Ja":
            zweiterButtonP_window.close()
            sg.Popup("Bitte Drücke zur Bestätigung die Hotkeys erneut!")
            mcd(ersterhotkey, zweiterhotkey, BButton)
            break
        if event == "Nein":
            sg.Popup("Versuchen wirs nochmal!")
            zweiterButtonP_window.close()
            zweiterButton(ersterhotkey)
        if event == sg.WIN_CLOSED:
            zweiterButtonP_window.close()
            break

def zweiterButton(ersterhotkey):
    zweiterButton_layout = [[sg.Text("Welcher soll dein zweiter Hotkey sein?")],
                            [sg.Push(),sg.Button("Zweiten Hotkey festlegen"),sg.Button("Ich möchte nur einen Hotkey"),sg.Push()]
                            ]
    zweiterButton_window = sg.Window("Multiclipboardduck", zweiterButton_layout)

    BButton = True
    while True: 
        event, values = zweiterButton_window.read()

        if event == sg.WIN_CLOSED:
            zweiterButton_window.close
            break
        if event == "Zweiten Hotkey festlegen":
            zweiterhotkey = kb.read_hotkey()
            keyboard.press(Key.ctrl)
            keyboard.press(Key.shift)
            zweiterButton_window.close()
            zweiterButtonP(ersterhotkey, zweiterhotkey, BButton)
            break
        if event == "Ich möchte nur einen Hotkey":
            BButton = False
            zweiterhotkey = 0
            zweiterButton_window.close()
            mcd(ersterhotkey, zweiterhotkey, BButton)
            break


def ersterButton(ersterhotkey):
    zweiButtons_layout = [[sg.Text("Du hast " + ersterhotkey + " gedrückt! Stimmt das?")],
                        [sg.Push(),sg.Button("Ja"), sg.Button("Nein"), sg.Push()]
    ]
    zweiButtons_window = sg.Window("Multiclipboardduck", zweiButtons_layout)

    while True:
        event, values = zweiButtons_window.read()

        if event == "Ja":
            zweiButtons_window.close()
            sg.Popup("Bitte Drücke zur Bestätigung die Hotkeys erneut!")
            zweiterButton(ersterhotkey)
            break
        if event == "Nein":
            sg.Popup("Versuchen wirs nochmal!")
            zweiButtons_window.close()
            greetw()
        if event == sg.WIN_CLOSED:
            zweiButtons_window.close()
            break


def greetw():

    global zweiterhotkey
    zweiterhotkey=""
    greetw_layout = [[sg.Text("Willkommen beim Multiclipboardduck!")],
                    [sg.Text("Welche Shortcuts/Hotkeys möchtest du verwenden? Bitte drücke den Button und danach die Hotkeys!")],
                    [sg.Text("Es wird empfohlen die Hotkeys \"Strg+Shift+E\" und \"Strg+Shift+W\" zu verwenden")],
                    [sg.Push(),sg.Button("Ersten Hotkey belegen", key = "-Button1-"),sg.Button("Empfohlene verwenden"),sg.Push()]
    ]

    greetw_window = sg.Window("Multiclipboardduck", greetw_layout)

    while True:
        event, values = greetw_window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "-Button1-":
            ersterhotkey = kb.read_hotkey()
            keyboard.press(Key.ctrl)
            keyboard.press(Key.shift)
            greetw_window.close()
            ersterButton(ersterhotkey)
            break
        if event == "Empfohlene verwenden":
            ersterhotkey = "Strg+Umschalt+E"
            BButton = True
            zweiterhotkey = "Strg+Umschalt+W"
            greetw_window.close()
            mcd(ersterhotkey, zweiterhotkey, BButton)
            break
greetw()
