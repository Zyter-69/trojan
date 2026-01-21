import atexit
import os
from jeu.snake import jeu

def cleanup():
    try:
        os.remove("trojan/Decrrojan.py")
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    atexit.register(cleanup)
    jeu()