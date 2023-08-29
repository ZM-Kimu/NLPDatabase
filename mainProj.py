import threading
import tkinter as tk
import ttkbootstrap as ttk
from time import sleep
from colorchange import animationObj
from ttkbootstrap.constants import *
from mainNLP import *


def updateAnimation():
    global screen_animationW
    root.update()
    screen_animationW = int(root.winfo_width())


def topLineAnimation(color):
    updateAnimation()
    topLineCanvas.delete("all")
    startPointL = screen_animationW/2
    startPointR = screen_animationW/2
    y = 3
    offset = 0
    tick = 0
    fillColor = color
    while True:
        topLineCanvas.delete('all')
        if startPointR < screen_animationW-screen_animationW/5:
            topLineCanvas.create_line(
                startPointL, y, startPointR, y, fill=fillColor, width=3)
        else:
            change = animationObj(fillColor, "#FFFFFF")
            topLineCanvas.delete("all")
            topLineCanvas.create_line(
                startPointL, y, startPointR, y, fill=change.gradient()[tick], width=3)
            tick += 1
            if tick >= len(change.gradient())-1:
                break
        startPointL -= offset
        startPointR += offset
        offset += 1
        topLineCanvas.update()
        topLineCanvas.after(12)


def textAnimation(color="#000000", textmode="show", text="", size=10):
    updateAnimation()
    middle = screen_animationW/2
    if textmode == "show":
        colorShow = animationObj("#FFFFFF", color)
        for i in colorShow.gradient():
            textCanvas.delete("all")
            textCanvas.create_text(
                middle, 25, text=text, fill=i, font=("黑体", size))
            textCanvas.after(10)
            textCanvas.update()
    elif textmode == "hide":
        colorShow = animationObj(color, "#FFFFFF")
        for i in colorShow.gradient():
            textCanvas.delete("all")
            textCanvas.create_text(
                middle, 25, text=text, fill=i, font=("黑体", size))
            textCanvas.after(10)
            textCanvas.update()


def showText(color, text, size, delay=1):
    sleep(0.5)
    textAnimation(color, "show", text, size)
    sleep(delay)
    textAnimation(color, "hide", text, size)


def showTextAndLine(colorText, text, size, delay, colorLine):
    global showText
    thread1 = threading.Thread(target=topLineAnimation, args=(colorLine,))
    thread2 = threading.Thread(
        target=showText, args=(colorText, text, size, delay))
    thread1.start()
    thread2.start()


def healthTheme(text):
    showTextAndLine("#8CC9C8", text, 14, 1, "#30B506")


def generalTheme(text):
    showTextAndLine("#5CCCC7", text, 14, 1, "#78C2CC")


def warningTheme(text):
    showTextAndLine("#F510CA", text, 14, 1, "#851836")


def enmergencyTheme(text):
    showTextAndLine("#FF0000", text, 14, 2, "#FF0000")


def destroying():
    sleep(2)
    root.destroy()
    exit()


def activateAnalyze():
    nlp = NLPCall(entry.get())
    if nlp.Prio == "normal":
        healthTheme(nlp.info)
    if nlp.Prio == "warning":
        generalTheme(nlp.info)
    if nlp.Prio == "middle":
        warningTheme(nlp.info)
    if nlp.Prio == "high":
        enmergencyTheme(nlp.info)
    if nlp.Prio == "exit":
        generalTheme(nlp.info)
        threading.Thread(target=destroying).start()


root = tk.Tk()
root.update()
root.title("自然语言可交互型数据库")
#style = ttk.Style(theme="litera")
# style.configure("ttk",background="green")
buttonClicked = False
#root.iconphoto(False, ttk.PhotoImage(file="gi.png"))
screen_W, screen_H = root.winfo_screenwidth(), root.winfo_screenheight()
window_W, window_H = int(screen_W/2), int(screen_H//3)
root.geometry(f"{window_W}x{window_H}")
#root.resizable(0, 0)

topLineCanvas = ttk.Canvas(root, width=9000, height=5)
textCanvas = ttk.Canvas(root, width=9000, height=100)
label = ttk.Label(root, text="请输入您的操作", font=("黑体", 10))
entry = ttk.Entry(root, width=window_W//28, justify="center")
textButton = ttk.Button(root, text="提交", command=activateAnalyze)


topLineCanvas.pack()
textCanvas.pack()
label.pack()
entry.pack()
textButton.pack(pady=15)

if entry.focus == True:
    print(entry.select_present)
    topLineAnimation


root.mainloop()
