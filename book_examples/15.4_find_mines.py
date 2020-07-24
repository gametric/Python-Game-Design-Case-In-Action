#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/7/22 9:40

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


class Model:
    def __init__(self, row, col):
        self.width = col
        self.height = row
        self.items = [[0 for c in range(col)] for r in range(row)]

    def set_item_value(self, r, c, value):
        self.items[r][c] = value

    def check_value(self, r, c, value):
        if self.items[r][c] == value:
            return True
        else:
            return False

    def count_value(self, r, c, value):
        count = 0
        if r - 1 >= 0 and c - 1 >= 0:
            if self.items[r - 1][c - 1] == value: count += 1
        if r - 1 >= 0 and c >= 0:
            if self.items[r - 1][c] == value: count += 1
        if r - 1 >= 0 and c + 1 <= self.width - 1:
            if self.items[r - 1][c + 1] == value: count += 1
        if c - 1 >= 0:
            if self.items[r][c - 1] == value: count += 1
        if c + 1 <= self.width - 1:
            if self.items[r][c + 1] == value: count += 1
        if r + 1 <= self.height - 1 and c - 1 >= 0:
            if self.items[r + 1][c - 1] == value: count += 1
        if r + 1 <= self.height - 1:
            if self.items[r + 1][c] == value: count += 1
        if r + 1 <= self.height - 1 and c + 1 <= self.width - 1:
            if self.items[r + 1][c + 1] == value: count += 1
        return count


class Mines(tk.Frame):
    def __init__(self, m, master=None):
        tk.Frame.__init__(self, master)
        self.model = m
        self.init_mine()
        self.grid()
        self.create_widgets()
        self.click_count = 0
        self.trick_speed = 100
        self.trickit()

    def create_widgets(self):
        # self.rowconfigure(self.model.height, weight=1)
        # self.columnconfigure(self.model.width, weight=1)
        self.button_groups = [[tk.Button(self, height=2, width=5, bg='green') for i in range(self.model.width)] for j in
                              range(self.model.height)]
        for r in range(self.model.height):
            for c in range(self.model.width):
                # self.button_groups[r][c].grid(row=r, column=c, sticky=(tk.W, tk.E, tk.N, tk.S))
                self.button_groups[r][c].grid(row=r, column=c, sticky=('w', 'e', 'n', 's'))
                self.button_groups[r][c].bind('<Button-1>', self.click_event)
                self.button_groups[r][c].bind('<Button-3>', self.right_click_event)
                self.button_groups[r][c]['padx'] = r
                self.button_groups[r][c]['pady'] = c

    def trickit(self):
        def rgb_to_hex(tmp):
            rgb = tmp.split(',')
            strs = '#'
            for i in rgb:
                num = int(i)
                strs += str(hex(num))[-2:].replace('x', '0').upper()
            return strs

        global luck_score
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        c_r = 255 if luck_score > 50 else random.randint(0, 255)
        c_g = 255 if luck_score < 0 else 0
        c_b = 255 if luck_score < -50 else random.randint(0, 255)
        current_color = rgb_to_hex('{}, {}, {}'.format(c_r, c_g, c_b))
        self.lab_time = tk.Label(self, text='{} 此刻你的幸运值余额是 {}'.format(current_time, luck_score), fg=current_color)
        self.lab_time.grid(row=self.model.height, column=self.model.width)
        self.lab_time.after(self.trick_speed, self.trickit)

    def show_all(self):
        for r in range(model.height):
            for c in range(model.width):
                self.button_groups[r][c]['state'] = tk.DISABLED
                self.show_one(r, c)

    def show_one(self, r, c):
        if model.check_value(r, c, 0):
            self.button_groups[r][c]['image'] = ''
            self.button_groups[r][c]['text'] = model.count_value(r, c, 1)
        else:
            self.button_groups[r][c]['image'] = mine_img
            self.button_groups[r][c]['text'] = 'Q'

    def recure_show(self, r, c):
        if 0 <= r <= self.model.height - 1 and 0 <= c <= self.model.width - 1:
            if model.check_value(r, c, 0) and self.button_groups[r][c]['state'] == tk.NORMAL and model.count_value(r, c,
                                                                                                                   1) == 0:
                # self.button_groups[r][c]['bd'] = 4
                self.button_groups[r][c]['state'] = tk.DISABLED
                self.button_groups[r][c]['disabledforeground'] = 'light blue'
                self.button_groups[r][c]['image'] = ''
                self.button_groups[r][c]['text'] = '0'
                self.button_groups[r][c]['bg'] = 'light blue'
                self.recure_show(r - 1, c - 1)
                self.recure_show(r - 1, c)
                self.recure_show(r - 1, c + 1)
                self.recure_show(r, c - 1)
                self.recure_show(r, c + 1)
                self.recure_show(r + 1, c - 1)
                self.recure_show(r + 1, c)
                self.recure_show(r + 1, c + 1)
            elif model.count_value(r, c, 1) != 0:
                # self.button_groups[r][c]['bd'] = 4
                self.button_groups[r][c]['state'] = tk.DISABLED
                self.button_groups[r][c]['disabledforeground'] = 'green'
                self.button_groups[r][c]['image'] = ''
                self.button_groups[r][c]['text'] = model.count_value(r, c, 1)
                self.button_groups[r][c]['bg'] = 'light blue'
        else:
            pass

    def click_event(self, event):
        global luck_score
        r = int(str(event.widget['padx']))
        c = int(str(event.widget['pady']))
        if self.button_groups[r][c]['state'] == tk.NORMAL:
            self.click_count += 1
        print(r, c, self.click_count)
        if model.check_value(r, c, 1):
            self.show_all()
            self.button_groups[r][c]['state'] = tk.NORMAL
            if self.click_count == 1:
                luck_score -= 50
                message = tkmsg.showinfo('hint', 'You Fail 难得一遇？！( ▼-▼ )')
                if message:
                    new()
            else:
                luck_score += 10
                message = tkmsg.showinfo('hint', 'You Fail 胜败乃兵家常事！……')
                if message:
                    new()
        else:
            self.recure_show(r, c)
            if self.victory():
                luck_score += 10
                message = tkmsg.showinfo('hint', 'You Win 安有常胜将军？哈哈哈~ ●”◡”●')
                if message:
                    new()

    def right_click_event(self, event):
        global luck_score
        r = int(str(event.widget['padx']))
        c = int(str(event.widget['pady']))
        print(r, c)
        if self.button_groups[r][c]['state'] == tk.NORMAL and self.button_groups[r][c]['text'] == 'F':
            self.button_groups[r][c]['image'] = ask_img
            self.button_groups[r][c]['text'] = 'A'
        elif self.button_groups[r][c]['state'] == tk.NORMAL and self.button_groups[r][c]['text'] == 'A':
            self.button_groups[r][c]['image'] = ''
            self.button_groups[r][c]['fg'] = 'green'
            self.button_groups[r][c]['text'] = 'N'
        elif self.button_groups[r][c]['state'] == tk.NORMAL:
            self.button_groups[r][c]['image'] = flag_img
            self.button_groups[r][c]['text'] = 'F'
        if self.victory():
            luck_score += 10
            message = tkmsg.showinfo('hint', 'You Win 安有常胜将军？哈哈哈~ ●”◡”●')
            if message:
                new()

    def victory(self):
        for r in range(model.height):
            for c in range(model.width):
                if self.button_groups[r][c]['state'] == tk.NORMAL and self.button_groups[r][c]['text'] != 'F':
                    return False
                if model.check_value(r, c, 0) and self.button_groups[r][c]['text'] == 'F':
                    return False
        return True

    def init_mine(self):
        print(model.width, model.height)
        n = random.randint(1, int(max(1, max(model.width, model.height) / min(model.width, model.height))))
        for r in range(model.height):
            for i in range(n):
                rancol = random.randint(0, model.width - 1)
                model.set_item_value(r, rancol, 1)

    def printf(self):
        print('map')
        for r in range(model.height):
            for c in range(model.width):
                print(model.items[r][c], end=' ')
            print('')


def new():
    global m, model
    m.grid_remove()
    # model = Model(10, 10)
    model = Model(random.randint(8, 11), random.randint(8, 11))
    m = Mines(model, root)
    m.printf()
    pass


if __name__ == '__main__':
    root = tk.Tk()
    model = Model(10, 10)
    menu = tk.Menu(root)
    root.config(menu=menu)
    filemenu = tk.Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    filemenu.add_command(label='New', command=new)
    # filemenu.add_separator()
    filemenu.add_command(label='Exit', command=root.quit)

    luck_score = 0
    im1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image_mines', 'mine.png')
    im2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image_mines', 'flag.png')
    im3 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image_mines', 'ask.png')
    mine_img = tk.PhotoImage(file=im1)
    flag_img = tk.PhotoImage(file=im2)
    ask_img = tk.PhotoImage(file=im3)
    m = Mines(model, root)
    m.printf()

    root.mainloop()
