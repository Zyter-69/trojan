import atexit
import os
from jeu.snake import jeu

def cleanup():
    try:
        os.remove("jeu/trojan.exe")
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    atexit.register(cleanup)
    jeu()