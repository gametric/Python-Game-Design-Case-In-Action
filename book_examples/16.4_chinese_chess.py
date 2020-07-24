#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/7/24 5:42

@author: tatatingting
"""


import os
import tkinter as tk
from tkinter import messagebox as tkmsg
import random
import sys
from threading import Timer
import time
import operator
import winsound
import numpy as np


'''
黑：将，士，象，车，马，炮，卒
红：帅，仕，相，车，马，炮，兵
'''


def set_my_turn(flag):
    global local_player
    is_my_turn = flag
    if local_player == '红':
        local_player = '黑'
        label1['text'] = '轮到黑方走'
    else:
        local_player = '红'
        label1['text'] = '轮到红方走'


def is_able_to_put(id, x, y, oldx, oldy):
    qi_name = dict_chessname[id][1]
    if qi_name == '将' or qi_name == '帅':
        if (x - oldx) * (y - oldy) != 0:
            return False
        if (abs(x - oldx) > 1) or (abs(y - oldy) > 1):
            return False
        if (x < 3) or (x > 5) or (3 <= y <= 6):
            return False
        return True
    if qi_name == '士' or qi_name == '仕':
        if (x - oldx) * (y - oldy) == 0:
            return False
        if (abs(x - oldx) > 1) or (abs(y - oldy) > 1):
            return False
        if (x < 3) or (x > 5) or (3 <= y <= 6):
            return False
        return True
    if qi_name == '象' or qi_name == '相':
        if (x - oldx) * (y - oldy) == 0:
            return False
        if (abs(x - oldx) != 2) or (abs(y - oldy) != 2):
            return False
        if qi_name == '相' and y < 5:
            return False
        if qi_name == '象' and y >= 5:
            return False
        i = 0
        j = 0
        if (x - oldx) == 2:
            i = x - 1
        if (x - oldx) == -2:
            i = x + 1
        if (y - oldy) == 2:
            j = y - 1
        if (y - oldy) == -2:
            j = y + 1
        if chessmap[i][j] != -1:
            return False
        return True
    if qi_name == '马':
        if (abs(x - oldx) * abs(y - oldy)) != 2:
            return False
        if (x - oldx) == 2:
            if chessmap[x-1][oldy] != -1:
                return False
        if (x - oldx) == -2:
            if chessmap[x+1][oldy] != -1:
                return False
        if (y - oldy) == 2:
            if chessmap[oldx][y-1] != -1:
                return False
        if (y - oldy) == -2:
            if chessmap[oldx][y+1] != -1:
                return False
        return True
    if qi_name == '车':
        if (x - oldx) * (y - oldy) != 0:
            return False
        if x != oldx:
            if oldx > x:
                t = x
                x = oldx
                oldx = t
            for i in range(oldx, x + 1):
                if i != x and i != oldx:
                    if chessmap[i][y] != -1:
                        return False
        if y != oldy:
            if oldy > y:
                t = y
                y = oldy
                oldy = t
            for j in range(oldy, y + 1):
                if j != y and j != oldy:
                    if chessmap[x][j] != -1:
                        return False
        return True
    if qi_name == '炮':
        swapflagx = False
        swapflagy = False
        if (x - oldx) * (y - oldy) != 0:
            return False
        c = 0
        if x != oldx:
            if oldx > x:
                swapflagx = True
                t = x
                x = oldx
                oldx = t
            for i in range(oldx, x + 1):
                if i != x and i != oldx:
                    if chessmap[i][y] != -1:
                        c += 1
        if y != oldy:
            if oldy > y:
                swapflagy = True
                t = y
                y = oldy
                oldy = t
            for j in range(oldy, y + 1):
                if j != y and j != oldy:
                    if chessmap[x][j] != -1:
                        c += 1
        if c > 1:
            return False
        if c == 0:
            if swapflagx:
                t = x
                x = oldx
                oldx = t
            if swapflagy:
                t = y
                y = oldy
                oldy = t
            if chessmap[x][y] != -1:
                return False
        if c == 1:
            if swapflagx:
                t = x
                x = oldx
                oldx = t
            if swapflagy:
                t = y
                y = oldy
                oldy = t
            if chessmap[x][y] == -1:
                return False
        return True
    if qi_name == '卒' or qi_name == '兵':
        if (x - oldx) * (y - oldy) != 0:
            return False
        if abs(x - oldx) > 1 or abs(y - oldy) > 1:
            return False
        if y >= 5 and (x - oldx) != 0 and qi_name == '兵':
            return False
        if y - oldy > 0 and qi_name == '兵':
            return False
        if y < 5 and x - oldx != 0 and qi_name == '卒':
            return False
        if y - oldy < 0 and qi_name == '卒':
            return False
        return True
    return True


def callback(event):
    global local_player, chessmap, rect1, rect2, first_chessid, second_chessid, x1, x2, y1, y2, first
    print('clicked at', event.x, event.y, local_player)
    x = (event.x - 15) // 76
    y = (event.y - 15) // 76
    print('clicked at', x, y, local_player)
    # 第一次点击
    if first:
        x1 = x
        y1 = y
        first_chessid = chessmap[x1][y1]
        # 非空的位置
        if not(chessmap[x1][y1] == -1):
            player = dict_chessname[first_chessid][0]
            # 己方棋子
            if player != local_player:
                print('单机成对方棋子了！')
                return
            rect1 = cv.create_rectangle(60 + 76 * x - 40,
                                        60 + y * 76 - 40,
                                        60 + 76 * x + 80 - 40,
                                        60 + y * 76 + 80 - 40,
                                        outline='red')
            print('第1次单击', first_chessid)
            first = False
    # 第二次点击
    else:
        x2 = x
        y2 = y
        second_chessid = chessmap[x2][y2]
        # 第二次点在了非空的位置
        if not(chessmap[x2][y2] == -1):
            player = dict_chessname[second_chessid][0]
            # 点了己方棋子，则更新第一个点击的棋子信息
            if player == local_player:
                first_chessid = chessmap[x2][y2]
                cv.delete(rect1)
                x1 = x
                y1 = y
                rect1 = cv.create_rectangle(60 + 76 * x - 40,
                                            60 + y * 76 - 40,
                                            60 + 76 * x + 80 - 40,
                                            60 + y * 76 + 80 - 40,
                                            outline='red')
                print('第2次单击', first_chessid)
                return
            # 点在对方棋子上
            else:
                if not(chessmap[x2][y2] == -1) and is_able_to_put(first_chessid, x2, y2, x1, y1):
                    print('可以吃子', x1, y1)
                    cv.move(first_chessid, 76 * (x2 - x1), 76* (y2 - y1))
                    chessmap[x1][y1] = -1
                    chessmap[x2][y2] = first_chessid
                    cv.delete(second_chessid)
                    cv.delete(rect1)
                    cv.delete(rect2)
                    first = True
                    if dict_chessname[second_chessid][1] == '将':
                        tkmsg.showinfo('hint', '红方赢了！')
                        label1['text'] = '红方赢了！'
                        return
                    if dict_chessname[second_chessid][1] == '帅':
                        tkmsg.showinfo('hint', '黑方赢了！')
                        label1['text'] = '黑方赢了！'
                        return
                    set_my_turn(False)
                else:
                    print('不能吃子')
                    label1['text'] = '不能吃子'
                    cv.delete(rect2)
        # 第二次点在了空的位置
        else:
            rect2 = cv.create_rectangle(60 + 76 * x - 40,
                                        60 + y * 76 - 40,
                                        60 + 76 * x + 80 - 40,
                                        60 + y * 76 + 80 - 40,
                                        outline='yellow')
            print('kkk', first_chessid)
            print('目标位置无棋子， 移动棋子', first_chessid, x2, y2, x1, y1)
            # 判断是否可以走棋
            if is_able_to_put(first_chessid, x2, y2, x1, y1):
                print('可以移动棋子', x1, y1)
                cv.move(first_chessid, 76 * (x2 - x1), 76 * (y2 - y1))
                chessmap[x1][y1] = -1
                chessmap[x2][y2] = first_chessid
                cv.delete(rect1)
                cv.delete(rect2)
                first = True
                set_my_turn(False)
            else:
                print('不符合走棋规则')
                tkmsg.showinfo('hint', '不符合走棋规则')
                cv.delete(rect2)
            return



root = tk.Tk()
cv = tk.Canvas(root, bg='white', width=720, height=800)
chessname = ['黑车', '黑马', '黑象', '黑士', '黑将', '黑士', '黑象', '黑马', '黑车', '黑卒', '黑炮',
             '红车', '红马', '红相', '红仕', '红帅', '红仕', '红相', '红马', '红车', '红兵', '红炮']
d1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image_chinese_chess')
imgs = [tk.PhotoImage(file=os.path.join(d1, chessname[i]+'.png')) for i in range(0, 22)]
chessmap = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1] for y in range(0, 10)]
dict_chessname = {}
local_player = '红'
first = True
is_my_turn = True
rect1 = 0
rect2 = 0
first_chessid = 0
img1 = tk.PhotoImage(file=os.path.join(d1, '棋盘.png'))

def draw_board():
    p1 = cv.create_image((0, 0), image=img1)
    cv.coords(p1, (360, 400))

def load_chess():
    global chessmap
    # black
    for i in range(0, 9):
        img = imgs[i]
        id = cv.create_image((60 + 76 * i, 60), image=img)
        dict_chessname[id] = chessname[i]
        chessmap[i][0] = id
    for i in range(0, 5):
        img = imgs[9]
        id = cv.create_image((60 + 76 * 2 * i, 60 + 3 * 76), image=img)
        chessmap[i*2][3] = id
        dict_chessname[id] = chessname[9]
    img = imgs[10]
    id = cv.create_image((60 + 76 * 1, 60 + 2 * 76), image=img)
    chessmap[1][2] = id
    dict_chessname[id] = chessname[10]
    id = cv.create_image((60 + 76 * 7, 60 + 2 * 76), image=img)
    chessmap[7][2] = id
    dict_chessname[id] = chessname[10]
    # red
    for i in range(0, 9):
        img = imgs[i + 11]
        id = cv.create_image((60 + 76 * i, 60 + 9 * 76), image=img)
        dict_chessname[id] = chessname[i + 11]
        chessmap[i][9] = id
    for i in range(0, 5):
        img = imgs[20]
        id = cv.create_image((60 + 76 * 2 * i, 60 + 6 * 76), image=img)
        chessmap[i*2][6] = id
        dict_chessname[id] = chessname[20]
    img = imgs[21]
    id = cv.create_image((60 + 76 * 1, 60 + 7 * 76), image=img)
    chessmap[1][7] = id
    dict_chessname[id] = chessname[21]
    id = cv.create_image((60 + 76 * 7, 60 + 7 * 76), image=img)
    chessmap[7][7] = id
    dict_chessname[id] = chessname[21]

draw_board()
load_chess()
print(dict_chessname)
cv.bind('<Button-1>', callback)
cv.pack()
label1 = tk.Label(root, fg='red', bg='white', text='红方先走')
label1['text'] = '红方先走'
label1.pack()
root.mainloop()
