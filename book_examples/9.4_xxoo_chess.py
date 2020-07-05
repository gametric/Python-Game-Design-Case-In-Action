#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/6/19 13:27

@author: tatatingting
"""


import tkinter as tk
from tkinter import messagebox as msgbox

import os


x = 'X'
o = 'O'
empty = ' '

computer = x
human = o


def ask_yes_no(question):
    response = None
    while response not in ('y', 'n'):
        response = input(question).lower()
    return response


def pieces():
    global computer, human
    go_first = ask_yes_no('玩家是否先走（y/n）：')
    if go_first == 'y':
        print('\n玩家先走.')
        human = x
        computer = o
    else:
        print('\n电脑机器人先走')
        human = o
        computer = x
    return computer, human


def new_board():
    board = []
    for square in range(9):
        board.append(empty)
    return board


def legal_moves(board):
    moves = []
    for square in range(9):
        if board[square] == empty:
            moves.append(square)
    return moves


def winner(board):
    ways_to_win = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )
    for row in ways_to_win:
        if board[row[0]] == board[row[1]] == board[row[2]] != empty:
            winner = board[row[0]]
            return winner
    if empty not in board:
            return 'TIE'
    return False


def computer_move(board, computer, human):
    board = board[:]
    best_moves = (4, 0, 2, 6, 8, 1, 3, 5, 7)
    for move in legal_moves(board):
        board[move] = computer
        if winner(board) == computer:
            print('电脑机器人下棋位置……', move)
            return move
        board[move] = empty
    for move in legal_moves(board):
        board[move] = human
        if winner(board) == human:
            print('电脑机器人下棋位置……', move)
            return move
        board[move] = empty
    for move in best_moves:
        if move in legal_moves(board):
            print('电脑机器人下棋位置……', move)
            return move


def draw_qipan():
    cv.create_line(0, 40, 120, 40)
    cv.create_line(0, 80, 120, 80)
    cv.create_line(0, 120, 120, 120)
    cv.create_line(40, 0, 40, 120)
    cv.create_line(80, 0, 80, 120)
    cv.create_line(120, 0, 120, 120)
    cv.pack()


def draw_game_image(board):
    for square in range(9):
        if board[square] == x:
            img1 = imgs[0]
            i = square % 3
            j = square // 3
            cv.create_image((i*40+20, j*40+20), image=img1)
            cv.pack()
        elif board[square] == o:
            img1 = imgs[1]
            i = square % 3
            j = square // 3
            cv.create_image((i * 40 + 20, j * 40 + 20), image=img1)
            cv.pack()


def callback(event):
    global computer, human, board
    print('clicked at', event.x, event.y)
    x = event.x // 40
    y = event.y // 40
    print('clicked at', x, y)
    legal = legal_moves(board)
    move = y*3+x
    if move not in legal:
        print('\n此位置已经落过子了')
        return
    board[move] = human
    if human == o:
        img = imgs[1]
    else:
        img = imgs[0]
    cv.create_image((x*40+20, y*40+20), image=img)
    cv.pack()
    if not winner(board):
        move = computer_move(board, computer, human)
        board[move] = computer
        draw_game_image(board)
    the_winner = winner(board)
    if the_winner == computer:
        print('电脑机器人赢！\n')
        msgbox.showinfo(title='提示', message='电脑机器人赢了！')
    elif the_winner == human:
        print('玩家赢！\n')
        msgbox.showinfo(title='提示', message='玩家赢了！')
    elif the_winner == 'TIE':
        print('平局和棋，游戏结束！\n')
        msgbox.showinfo(title='提示', message='平局和棋，游戏结束！')


root = tk.Tk()
filename_x = os.path.join('image_xxoo', 'x.png')
filename_o = os.path.join('image_xxoo', 'o.png')
imgs = [tk.PhotoImage(file=filename_x), tk.PhotoImage(file=filename_o)]
cv = tk.Canvas(root, bg='green', width=226, height=226)
cv.pack()
cv.focus_set()

computer, human = pieces()
turn = x
draw_qipan()
board = new_board()

if turn == human:
    pass
else:
    move = computer_move(board, computer, human)
    board[move] = computer

draw_game_image(board)

cv.bind('<Button-1>', callback)

root.mainloop()
