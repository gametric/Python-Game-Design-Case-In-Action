#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/7/4 16:33

@author: tatatingting
"""


import copy
import tkinter as tk
import os
from tkinter import messagebox as tkmsg


def draw_game_image():
    global x, y, myArray
    print(myArray)
    for i in range(7):
        for j in range(7):
            if myArray[i][j] == worker:
                x = i
                y = j
                print('工人当前的位置是： ', x, y)
            img1 = imgs[myArray[i][j]]
            cv.create_image(i*p_w+p_w, j*p_w+p_w, image=img1)
            cv.pack()


def move_man(x, y):
    global myArray
    if myArray[x][y] == worker:
        myArray[x][y] = passageway
    elif myArray[x][y] == worker_indest:
        myArray[x][y] = destination
    # print(myArray)

def is_finish():
    global myArray
    b_finish = True
    for i in range(7):
        for j in range(7):
            if myArray[i][j] == destination or myArray[i][j] == worker_indest:
                b_finish = False
    return b_finish


def is_in_game_area(row, col):
    return (row>=0 and row<7 and col>=0 and col<7)


def move_to(x1, y1, x2, y2):
    global x, y, myArray
    p1 = None
    p2 = None
    if is_in_game_area(x1, y1):
        p1 = myArray[x1][y1]
    if is_in_game_area(x2, y2):
        p2 = myArray[x2][y2]
    if p1 == passageway:
        move_man(x, y)
        x = x1
        y = y1
        myArray[x1][y1] = worker
    if p1 == destination:
        move_man(x, y)
        x = x1
        y = y1
        myArray[x1][y1] = worker_indest
    if p1 == wall or not is_in_game_area(x1, y1):
        return
    if p1 == box:
        if p2 == wall or not is_in_game_area(x2, y2) or p2 == box:
            return
    if p1 == box and p2 == passageway:
        move_man(x, y)
        x = x1
        y = y1
        myArray[x1][y1] = worker
        myArray[x2][y2] = box
    if p1 == box and p2 == destination:
        move_man(x, y)
        x = x1
        y = y1
        myArray[x1][y1] = worker
        myArray[x2][y2] = redbox
    draw_game_image()
    if is_finish():
        tkmsg.showinfo(title='提示', message='恭喜你顺利过关')
        print('下一关')


def callback(event):
    global x, y, myArray

    key_code = event.keysym
    print('按下键： ', event.keysym)

    if key_code=='Up':
        x1 = x
        y1 = y - 1
        x2 = x
        y2 = y - 2
        move_to(x1, y1, x2, y2)
    elif key_code == 'Down':
        x1 = x
        y1 = y + 1
        x2 = x
        y2 = y + 2
        move_to(x1, y1, x2, y2)
    elif key_code == 'Right':
        x1 = x + 1
        y1 = y
        x2 = x + 2
        y2 = y
        move_to(x1, y1, x2, y2)
    elif key_code == 'Left':
        x1 = x - 1
        y1 = y
        x2 = x - 2
        y2 = y
        move_to(x1, y1, x2, y2)
    elif key_code == 'space':
        myArray = copy.deepcopy(myArray1)
        draw_game_image()
        print('已重新开始')


root = tk.Tk()
root.title('PYTHON PUSH BOX 推箱子')

# 原始地图
myArray1 = [[0, 3, 1, 4, 3, 3, 3],
            [0, 3, 3, 2, 3, 3, 0],
            [0, 0, 3, 0, 3, 3, 0],
            [3, 3, 2, 3, 0, 0, 0],
            [3, 4, 3, 3, 3, 0, 0],
            [0, 0, 3, 3, 3, 3, 0],
            [0, 0, 0, 0, 0, 0, 0]]

wall = 0
worker = 1
box = 2
passageway = 3
destination = 4
worker_indest = 5
redbox = 6

imgs = [tk.PhotoImage(file=os.path.join('image_pushbox', '0_wall.png')),
        tk.PhotoImage(file=os.path.join('image_pushbox', '1_worker.png')),
        tk.PhotoImage(file=os.path.join('image_pushbox', '2_box.png')),
        tk.PhotoImage(file=os.path.join('image_pushbox', '3_passageway.png')),
        tk.PhotoImage(file=os.path.join('image_pushbox', '4_destination.png')),
        tk.PhotoImage(file=os.path.join('image_pushbox', '5_worker_indest.png')),
        tk.PhotoImage(file=os.path.join('image_pushbox', '6_redbox.png'))]
p_w = 50

cv = tk.Canvas(root, bg='green', width=400, height=400)
myArray=copy.deepcopy(myArray1)
draw_game_image()
cv.bind('<KeyPress>', callback)
cv.pack()
cv.focus_set()
root.mainloop()
