from tkinter import *
import webbrowser


def __init__(ip_addr):
    root = Tk()
    root.title("GG")
    text = Text(root)
    text.insert(END, "Sigin: "+ip_addr+":8081\nOpen Browser!!")
    text.pack()
    webbrowser.open("http://"+ip_addr+":8081")
    root.mainloop()