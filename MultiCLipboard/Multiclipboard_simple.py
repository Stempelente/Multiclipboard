from unittest.loader import VALID_MODULE_NAME
import PySimpleGUI as sg
import pyperclip as pc
import keyboard as kb
import textwrap

a = ""
b = ""

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
                event, values = window.read(timeout=5)
                if event != sg.TIMEOUT_KEY:
                    window.set_alpha(1)
                    break
            event, values = window(timeout=display_duration_in_ms)
            if event == sg.TIMEOUT_KEY:
                for i in range(int(alpha*100),1,-1):       # fade out
                    window.set_alpha(i/100)
                    event, values = window.read(timeout=5)
                    if event != sg.TIMEOUT_KEY:
                        break
        else:
            window.set_alpha(alpha)
            event, values = window(timeout=display_duration_in_ms)

        window.close()

    if __name__ == '__main__':
        title = "Multiclipduck"
        message = "Es wurde: \"" + c + "\" in den Cache geladen." 
        display_notification(title, message, img_success, 500, use_fade_in=True)


layout = [[sg.Text("Speicher A: "), sg.InputText(), sg.Button("Speicher A")],
            [sg.Text("Speicher B: "), sg.InputText(), sg.Button("Speicher B")]
            ]

window = sg.Window("Multiclipboard", layout)

while True:
    event, values = window.read(timeout=100)

    if event == "Speicher A":
        a = values[0]

    if event == "Speicher B":
        b = values[1]

    if not a == "":
        if kb.is_pressed("ctrl+shift+e"):
            pc.copy(values[0])
            c = a
            fadeaway()

        elif kb.is_pressed("ctrl+shift+w"):
            pc.copy(values[1])
            c = b
            fadeaway()





    if event == sg.WIN_CLOSED:
        #sg.Popup("Das war's ich bin tot.")
        break