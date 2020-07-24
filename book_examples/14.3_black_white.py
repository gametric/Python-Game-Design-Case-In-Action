#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/7/18 16:37

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


def get_new_board():
    board = []
    for i in range(8):
        board.append(['none'] * 8)
    return board


def reset_board(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = 'none'
    board[3][3] = 'black'
    board[3][4] = 'white'
    board[4][3] = 'white'
    board[4][4] = 'black'


def who_go_first():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def is_on_board(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


def is_valid_move(board, tile, x, y):
    if not is_on_board(x, y) or board[x][y] != 'none':
        return False
    board[x][y] = tile
    if tile == 'black':
        other_tile = 'white'
    else:
        other_tile = 'black'
    tiles_to_filp = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x0, y0 = x, y
        x0 += xdirection
        y0 += ydirection
        if is_on_board(x0, y0) and board[x0][y0] == other_tile:
            x0 += xdirection
            y0 += ydirection
            if not is_on_board(x0, y0):
                continue
            while board[x0][y0] == other_tile:
                x0 += xdirection
                y0 += ydirection
                if not is_on_board(x0, y0):
                    break
            if not is_on_board(x0, y0):
                continue
            if board[x0][y0] == tile:
                while True:
                    x0 -= xdirection
                    y0 -= ydirection
                    if x0 == x and y0 == y:
                        break
                    tiles_to_filp.append([x0, y0])
    board[x][y] = 'none'
    if len(tiles_to_filp) == 0:
        return False
    return tiles_to_filp


def get_valid_moves(board, tile):
    valid_moves = []
    for x in range(8):
        for y in range(8):
            if is_valid_move(board, tile, x, y) != False:
                valid_moves.append([x, y])
    return valid_moves


def get_score_of_board(board):
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == 'black':
                    xscore += 1
                if board[x][y] == 'white':
                    oscore += 1
        return {'black': xscore, 'white': oscore}


def make_move(board, tile, x, y):
    tiles_to_flip = is_valid_move(board, tile, x, y)
    if tiles_to_flip == False:
        return False
    board[x][y] = tile
    for x, y in tiles_to_flip:
        board[x][y] = tile
    return True


def get_computer_move(board, computer_tile):
    def is_on_corner(x, y):
        return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

    def get_board_copy(board):
        dupe_board = get_new_board()
        for x in range(8):
            for y in range(8):
                dupe_board[x][y] = board[x][y]
        return dupe_board

    possible_moves = get_valid_moves(board, computer_tile)
    if not possible_moves:
        print('电脑机器人没有合法走法')
        return None
    random.shuffle(possible_moves)
    for x, y in possible_moves:
        if is_on_corner(x, y):
            return [x, y]
    best_score = -1
    best_move = None
    for x, y in possible_moves:
        dupe_board = get_board_copy(board)
        make_move(dupe_board, computer_tile, x, y)
        score = get_score_of_board(dupe_board)[computer_tile]
        if score > best_score:
            best_move = [x, y]
            best_score = score
    return best_move


def computer_go():
    global turn
    if (not game_over) and (turn == 'computer'):
        x, y = get_computer_move(main_board, computer_tile)
        make_move(main_board, computer_tile, x, y)
        # savex, savey = x, y
        if get_valid_moves(main_board, player_tile) != []:
            turn = 'player'
        else:
            if get_valid_moves(main_board, computer_tile) != []:
                tkmsg.showinfo('电脑机器人继续', message='电脑机器人继续')
                computer_go()
            else:
                tkmsg.showinfo('?', message='???')


def draw_all_again():
    def draw_qi_pan():
        cv.create_image((360, 360), image=imgs[2])
        cv.pack()

    draw_qi_pan()
    for x in range(8):
        for y in range(8):
            if main_board[x][y] == 'black':
                cv.create_image((x * 80 + 80, y * 80 + 80), image=imgs[0])
                cv.pack()
            elif main_board[x][y] == 'white':
                cv.create_image((x * 80 + 80, y * 80 + 80), image=imgs[1])
                cv.pack()


def draw_can_go():
    list1 = get_valid_moves(main_board, player_tile)
    for m in list1:
        x = m[0]
        y = m[1]
        cv.create_image((x * 80 + 80, y * 80 + 80), image=imgs[3])
        cv.pack()


def callback(event):
    def is_game_over(board):
        for x in range(8):
            for y in range(8):
                if board[x][y] == 'none':
                    return False
        return True

    global turn
    if (not game_over) and (turn == 'computer'):
        return
    col = int((event.x - 40) / 80)
    row = int((event.y - 40) / 80)
    if main_board[col][row] != 'none':
        tkmsg.showinfo('提示', message='已有棋子')
    if make_move(main_board, player_tile, col, row):
        if get_valid_moves(main_board, computer_tile) != []:
            turn = 'computer'
    if get_computer_move(main_board, computer_tile) == None:
        turn = 'player'
        tkmsg.showinfo('玩家继续', '玩家继续')
    else:
        computer_go()

    draw_all_again()
    draw_can_go()
    if is_game_over(main_board):
        score_player = get_score_of_board(main_board)[player_tile]
        score_computer = get_score_of_board(main_board)[computer_tile]
        out_put = game_over_str + '玩家： ' + str(score_player) + ': ' + '电脑机器人： ' + str(score_computer)
        tkmsg.showinfo('游戏结束提示', message=out_put)


root = tk.Tk('人机黑白棋')
im1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image_black_white', 'black.png')
im2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image_black_white', 'white.png')
im3 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image_black_white', 'board.png')
im4 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image_black_white', 'info.png')
imgs = [tk.PhotoImage(file=im1), tk.PhotoImage(file=im2), tk.PhotoImage(file=im3), tk.PhotoImage(file=im4)]
game_over = False
game_over_str = 'Game Over Score! '
main_board = get_new_board()
reset_board(main_board)
turn = who_go_first()
tkmsg.showinfo('游戏开始提示', turn+'先走！')
print(turn, '先走！')
if turn == 'player':
    player_tile = 'black'
    computer_tile = 'white'
else:
    player_tile = 'white'
    computer_tile = 'black'
    computer_go()
cv = tk.Canvas(root, bg='green', width=720, height=780)
draw_all_again()
draw_can_go()
cv.bind('<Button-1>', callback)
cv.pack()
root.mainloop()
