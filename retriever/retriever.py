import os
import json
import tkinter

home = os.path.expanduser("~")
data_file = os.path.join(home, "silliness.json")

with open(data_file, "r") as f:
    key = json.load(f)["key"]

class Window(tkinter.Tk):
    def __init__(self, key):
        super().__init__()

        self.title("doge key retrieval tool")
        self.resizable(0, 0)

        self.text = tkinter.Text(self, height=3)
        self.text.insert(1.0, f"Even though Doge is not a golden retriever, he has retrieved your key:\n{key}\nPut this key into sillyquip.exe and it will unlock your files :)")
        self.text.configure(state="disabled")
        self.text.configure(inactiveselectbackground=self.text.cget("selectbackground"))
        self.text.pack(padx=10, pady=10)

win = Window(key)
win.mainloop()