#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/6/7 10:33

@author: tatatingting
"""

import tkinter as tk
import sys
import random
import re


number = random.randint(0, 1024)
running = True
num = 0
nmaxn = 1024
nminn = 0


def eBtnGuess(event):
    global nmaxn
    global nminn
    global num
    global running
    if running:
        val_a = int(entry_a.get())
        if val_a == number:
            labelqval("恭喜答对了！")
            num += 1
            running = False
            numGuess()  # 显示猜的次数
        elif val_a < number:
            if val_a > nminn:
                nminn = val_a
                num += 1
                labelqval("小了哦，请输入" + str(nminn) + "到" + str(nmaxn) + "之间任意整数： ")
        else:
            if val_a < nmaxn:
                nmaxn = val_a
                num += 1
                labelqval("大了哦，请输入" + str(nminn) + "到" + str(nmaxn) + "之间任意整数： ")
    else:
        labelqval("你已经答对啦……")


def numGuess():
    if num == 1:
        labelqval("厉害！一次答对！")
    elif num < 10:
        labelqval("= = 十次以内就答对了，很棒……")
    else:
        labelqval("好吧，你都尝试了超过十次了")


def labelqval(vText):
    label_val_q.config(label_val_q, text=vText)


def eBtnClose(event):
    root.destroy()


root = tk.Tk(className="猜数字游戏")
root.geometry("400x90+200+200")

label_val_q = tk.Label(root, width="80")  # 提示标签
label_val_q.pack(side="top")

entry_a = tk.Entry(root, width="40")  # 猜文本输入框
btnGuess = tk.Button(root, text="猜")  # 猜按钮

entry_a.bind('<Return>', eBtnGuess)
entry_a.pack(side="left")
btnGuess.bind('<Button-1>', eBtnGuess)
btnGuess.pack(side="left")

btnClose = tk.Button(root, text="关闭")  # 关闭按钮
btnClose.bind('<Button-1>', eBtnClose)
btnClose.pack(side="left")

labelqval("请输入0~1024的任意整数： ")
entry_a.focus_set()
print(number)
root.mainloop()
