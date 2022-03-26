from tkinter import *

def field(width):
    root = Tk()
    root.geometry("1200x900")
    Can = Canvas(root,width=1200,height=900)
    Can.pack()
    for x in range(width,900,width):
        l = Can.create_line(x,0,x,900,fill='black')
    for y in range(width,900,width):
        l = Can.create_line(0,y,900,y)
    l = l = Can.create_line(900,0,900,900,fill='black')
    return root,Can