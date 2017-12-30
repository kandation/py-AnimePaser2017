from tkinter import *
import webbrowser


def __init__():
    root = Tk()
    root.title("GG")
    text = Text(root)
    text.insert(END, "Sigin: 127.0.0.1:8081\nOpen Browser!!")
    text.pack()
    webbrowser.open("http://127.0.0.1:8081")
    root.mainloop()