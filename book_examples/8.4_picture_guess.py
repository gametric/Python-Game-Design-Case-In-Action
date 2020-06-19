# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/6/18 19:24

@author: tatatingting
"""

import random

from PIL import Image
import os

import tkinter as tk
from tkinter import messagebox as msgbox


def splitimage(src, rownum, colnum, dstpath):
    img = Image.open(src)
    w, h = img.size

    if rownum <= h and colnum <= w:
        print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
        print('开始处理图片切割，请稍候……')

        s = os.path.split(src)

        if dstpath == '':
            dstpath = s[0]

        fn = s[1].split('.')
        basename = fn[0]
        ext = fn[-1]
        num = 0
        rowheight = h // rownum
        colwidth = w // colnum

        for r in range(rownum):
            for c in range(colnum):
                box = (c * colwidth, r * rowheight, (c + 1) * colwidth, (r + 1) * rowheight)
                img.crop(box).save(os.path.join(dstpath, basename + '_' + str(num) + '.' + ext))
                num += 1
        print('图片切割完毕，共生产 %s 张小图片。' % num)

    else:
        print('不合法的行列切割参数！')


def get_imagesplit():
    src = input('请输入图片文件路径：')  # image_guess/pic_0.png
    if os.path.isfile(src):
        dstpath = input('请输入图片输出目录（不输入路径则表示使用源图片所在目录）：')
        if (dstpath == '') or os.path.exists(dstpath):
            row = int(input('请输入切割行数： '))
            col = int(input('请输入切割烈数： '))
            if row > 0 and col > 0:
                splitimage(src, row, col, dstpath)
            else:
                print('无效的行列切割参数！')
        else:
            print('图片输出目录 %s 不存在！' % dstpath)
    else:
        print('图片文件 %s 不存在!' % src)


# get_imagesplit()


width = 312
height = 450

image_width = width // 3
image_height = height // 3

rows = 3
cols = 3
steps = 0

board = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

root = tk.Tk('拼图2020')
root.title('拼图游戏程序设计练习')

pics = []
for i in range(9):
    filename = os.path.join('image_guess', 'pic_0_' + str(i) + '.png')
    pics.append(tk.PhotoImage(file=filename))


class Square:
    def __init__(self, orderID):
        self.orderID = orderID

    def draw(self, canvas, board_pos):
        img = pics[self.orderID]
        canvas.create_image(board_pos, image=img)


def init_board():
    L = list(range(9))
    random.shuffle(L)

    for i in range(rows):
        for j in range(cols):
            idx = i * rows + j
            orderID = L[idx]
            if orderID is 8:
                board[i][j] = None
            else:
                board[i][j] = Square(orderID)


def drawBoard(canvas):
    canvas.create_polygon((0, 0, width, 0, width, height, 0, height), width=1, outline='Blue')
    for i in range(rows):
        for j in range(cols):
            if board[i][j] is not None:
                board[i][j].draw(canvas, (image_width*(j+0.5), image_height*(i+0.5)))


def win():
    for i in range(rows):
        for j in range(cols):
            if board[i][j] is not None and board[i][j].orderID != i*rows+j:
                return False
    return True


def mouseclick(pos):
    global steps

    r = int(pos.y // image_height)
    c = int(pos.x // image_width)
    if r < 3 and c < 3:
        if board[r][c] is None:
            return
        else:
            current_square = board[r][c]
            if r-1 >= 0 and board[r-1][c] is None:
                board[r][c] = None
                board[r-1][c] = current_square
                steps += 1
            elif c+1 <=2 and board[r][c+1] is None:
                board[r][c] = None
                board[r][c+1] = current_square
                steps += 1
            elif r+1 <= 2 and board[r+1][c] is None:
                board[r][c] = None
                board[r+1][c] = current_square
                steps += 1
            elif c-1 >= 0 and board[r][c-1] is None:
                board[r][c] = None
                board[r][c-1] = current_square
                steps += 1
            # print(board)
            label1['text'] = '步数: ' + str(steps)
            cv.delete('all')
            drawBoard(cv)
    if win():
        msgbox.showinfo(title='恭喜', message='你成功了！')


def play_game():
    global steps
    steps = 0
    init_board()


def callBack2():
    print('重新开始')
    play_game()
    cv.delete('all')
    drawBoard(cv)


cv = tk.Canvas(root, bg='green', width=width, height=height)
b1 = tk.Button(root, text='重新开始', command=callBack2, width=20)
b1.pack()
label1 = tk.Label(root, text='步数： ' + str(steps), fg='red', width=20)
label1.pack()

cv.bind('<Button-1>', mouseclick)
# cv.find
cv.pack()

play_game()
drawBoard(cv)

root.mainloop()
