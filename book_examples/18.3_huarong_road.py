#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/7/27 13:36

@author: tatatingting
"""

import os
import tkinter as tk
from tkinter import messagebox as tkmsg
import random


class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y


class Block(tk.Button):
    def __init__(self, p, blockType, master, r, bm):
        tk.Button.__init__(self, master)
        self.Location = p
        self.BType = blockType
        self['text'] = r
        self['image'] = bm
        self.bind('<ButtonPress>', btn_MouseDown)
        self.bind('<ButtonRelease>', btn_Realse)
        self.place(x=self.Location.X * 80, y=self.Location.Y * 80)

    def GetPoints(self):
        pList = []
        if self.BType == One:
            pList.append(self.Location)
        elif self.BType == TwoH:
            pList.append(self.Location)
            pList.append(Point(self.Location.X + 1, self.Location.Y))
        elif self.BType == TwoV:
            pList.append(self.Location)
            pList.append(Point(self.Location.X, self.Location.Y + 1))
        elif self.BType == Four:
            pList.append(self.Location)
            pList.append(Point(self.Location.X + 1, self.Location.Y))
            pList.append(Point(self.Location.X, self.Location.Y + 1))
            pList.append(Point(self.Location.X + 1, self.Location.Y + 1))
        return pList

    def Contains(self, point):
        pList = self.GetPoints()
        for i in range(len(pList)):
            if pList[i].x == point.x and pList[i].y == point.y:
                return True
        return False

    def Intersects(self, block):
        myPoints = self.GetPoints()
        otherPoints = block.GetPoints()
        for i in range(len(otherPoints)):
            p = otherPoints[i]
            for j in range(len(myPoints)):
                if p.X == myPoints[j].X and p.Y == myPoints[j].Y:
                    return True
        return False

    def IsValid(self, width, height):
        points = self.GetPoints()
        for i in range(len(points)):
            p = points[i]
            if p.X < 0 or p.X >= width or p.Y < 0 or p.Y >= height:
                return False
        return True


class Game():
    Width = 4
    Height = 5
    WinFlag = False
    Blocks = []
    finishPoint = Point(1, 3)

    def GetBlockByPos(self, p):
        for i in range(len(self.Blocks)):
            if self.Blocks[i].Location.X == p.X and self.Blocks[i].Location.Y == p.Y:
                return self.Blocks[i]
        return False

    def AddBlock(self, block):
        if block in self.Blocks:
            return False
        if not block.IsValid(self.Width, self.Height):
            return False
        for i in range(len(self.Blocks)):
            if self.Blocks[i].Intersects(block):
                return False
        self.Blocks.append(block)
        return  True

    def MoveBlock(self, block, direction):
        if block not in self.Blocks:
            print('非此游戏中的块！')
            return
        oldx = block.Location.X
        oldy = block.Location.Y
        if direction == 'Up':
            block.Location.Y -= 1
        elif direction == 'Down':
            block.Location.Y += 1
        elif direction == 'Left':
            block.Location.X -= 1
        elif direction == 'Right':
            block.Location.X += 1
        moveOK = True
        if not block.IsValid(self.Width, self.Height):
            moveOK = False
        else:
            for i in range(len(self.Blocks)):
                if block is not self.Blocks[i] and block.Intersects(self.Blocks[i]):
                    moveOK = False
                    break
            if not moveOK:
                print('不能移动！')
                print(block.Location.X, block.Location.Y)
                block.Location = Point(oldx, oldy)
                print(block.Location.X, block.Location.Y)
            if moveOK:
                print(block['text'], block.Location.X, block.Location.Y)
                if block['text'] == '曹操' and block.Location.X == 1 and block.Location.Y == 3:
                    self.WinFlag = True
        return moveOK

    def GameWin(self):
        if self.WinFlag:
            return True
        else:
            return False


def btn_MouseDown(event):
    global mouseDownPoint, mouseDown
    mouseDownPoint = Point(event.x, event.y)
    mouseDown = True


def btn_Realse(event):
    global mouseDownPoint, mouseDown
    print(event.x, event.y)
    if not mouseDown:
        return
    moveH = event.x - mouseDownPoint.X
    moveV = event.y - mouseDownPoint.Y
    x = int(event.widget.place_info()['x'])//80
    y = int(event.widget.place_info()['y'])//80
    block = game.GetBlockByPos(Point(x, y))
    if moveH >= BlockSize * 1 / 3:
        game.MoveBlock(block, 'Right')
    elif moveH <= -BlockSize * 1 / 3:
        game.MoveBlock(block, 'Left')
    elif moveV >= BlockSize * 1 / 3:
        game.MoveBlock(block, 'Down')
    elif moveV <= -BlockSize * 1 / 3:
        game.MoveBlock(block, 'Up')
    else:
        return
    event.widget.place(x=block.Location.X * 80, y=block.Location.Y * 80)
    if game.GameWin():
        print('游戏胜利')
    mouseDown = False


BlockSize = 80
mouseDownPoint = Point(0, 0)
mouseDown = False

One = 1
TwoH = 2
TwoV = 3
Four = 4

win = tk.Tk()
win.title('华容道游戏')
win.geometry('320x400')
game = Game()
dir1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image_huarong_road')
bm = [tk.PhotoImage(file=os.path.join(dir1, '曹操.png')),
      tk.PhotoImage(file=os.path.join(dir1, '关羽.png')),
      tk.PhotoImage(file=os.path.join(dir1, '黄忠.png')),
      tk.PhotoImage(file=os.path.join(dir1, '马超.png')),
      tk.PhotoImage(file=os.path.join(dir1, '张飞.png')),
      tk.PhotoImage(file=os.path.join(dir1, '赵云.png')),
      tk.PhotoImage(file=os.path.join(dir1, '兵.png'))]
b0 = Block(Point(1, 0), Four, win, '曹操', bm[0])
b1 = Block(Point(1, 2), TwoH, win, '关羽', bm[1])
b2 = Block(Point(3, 2), TwoV, win, '黄忠', bm[2])
b3 = Block(Point(0, 0), TwoV, win, '马超', bm[3])
b4 = Block(Point(0, 2), TwoV, win, '张飞', bm[4])
b5 = Block(Point(3, 0), TwoV, win, '赵云', bm[5])
b6 = Block(Point(0, 4), One, win, '兵', bm[6])
b7 = Block(Point(1, 3), One, win, '兵', bm[6])
b8 = Block(Point(2, 3), One, win, '兵', bm[6])
b9 = Block(Point(3, 4), One, win, '兵', bm[6])
game.AddBlock(b0)
game.AddBlock(b1)
game.AddBlock(b2)
game.AddBlock(b3)
game.AddBlock(b4)
game.AddBlock(b5)
game.AddBlock(b6)
game.AddBlock(b7)
game.AddBlock(b8)
game.AddBlock(b9)
win.mainloop()
