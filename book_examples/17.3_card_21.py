#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/7/25 14:09

@author: tatatingting
"""

import os
import tkinter as tk
from tkinter import messagebox as tkmsg
import random


class Card(tk.Button):
    def __init__(self, x, y, face, suit_type, master, bm):
        tk.Button.__init__(self, master)
        self.x = x
        self.y = y
        self.face = face
        self.suit_type = suit_type
        self.place(x=self.x * 18, y=self.y * 20 + 150)
        if face < 10:
            self.count = face + 1
        else:
            self.count = 10
        self.faceup = False
        self.img = bm
        if self.faceup:
            self['image'] = bm
        else:
            self['image'] = back

    def draw_card(self, x, y):
        self.place(x=x, y=y)
        self['image'] = self.img

    def remove_card(self):
        self.place(x=-100, y=-100)


def callback1(event):
    global top_card, ip_card, id_card, dealer_ace, player_ace, dealer_count, player_count
    dealer_ace = 0
    player_ace = 0
    dealer_count = 0
    player_count = 0
    if top_card > 0:
        for i in range(top_card):
            deck[i].remove_card()

    deck[top_card].draw_card(200, 300)
    player_count = player_count + deck[top_card].count
    if deck[top_card].face == 0:
        player_count += 10
        player_ace += 1
    top_card += 1

    deck[top_card].draw_card(200, 10)
    dealer_count = dealer_count + deck[top_card].count
    if deck[top_card].face == 0:
        dealer_count += 10
        dealer_ace += 1
    top_card += 1

    deck[top_card].draw_card(265, 300)
    player_count = player_count + deck[top_card].count
    if deck[top_card].face == 0:
        player_count += 10
        player_ace += 1
    top_card += 1

    deck[top_card].draw_card(265, 10)
    dealer_count = dealer_count + deck[top_card].count
    if deck[top_card].face == 0:
        dealer_count += 10
        dealer_ace += 1
    top_card += 1

    ip_card = 2
    id_card = 2
    if top_card >= 52:
        tkmsg.showinfo('hint', '一副牌发完了')
        return

    label1['text'] = '玩家' + str(player_count)
    label2['text'] = '庄家' + str(dealer_count)
    bt1['state'] = tk.DISABLED
    bt2['state'] = tk.NORMAL
    bt3['state'] = tk.NORMAL


def callback2(event):
    global top_card, ip_card, dealer_ace, dealer_count, player_ace, player_count
    deck[top_card].draw_card(200 + 65 * ip_card, 300)
    player_count += deck[top_card].count
    if deck[top_card].face == 0:
        player_count += 10
        player_ace += 1
    top_card += 1
    if top_card >= 52:
        tkmsg.showinfo('hint', '一副牌发完了')
        return
    ip_card += 1
    label1['text'] = '玩家' + str(player_count)
    if player_count > 21:
        if player_ace >= 1:
            player_count -= 10
            player_ace -= 1
            label1['text'] = '玩家' + str(player_count)
    else:
        tkmsg.showinfo('hint', '玩家输了！')
        bt1['state'] = tk.NORMAL
        bt2['state'] = tk.DISABLED
        bt3['state'] = tk.DISABLED


def callback3(event):
    dealer_play()


def dealer_play():
    global top_card, id_card, dealer_ace, dealer_count, player_ace, player_count
    while True:
        if dealer_count < 18:
            deck[top_card].draw_card(200 + 65 * id_card, 10)
            dealer_count += deck[top_card].count
            if dealer_count > 21 and dealer_ace >= 1:
                dealer_count -= 10
                dealer_ace -= 1
            if deck[top_card].face == 0 and dealer_count <= 11:
                dealer_count += 10
                dealer_ace += 1
            top_card += 1
            if top_card >= 52:
                tkmsg.showinfo('hint', '一副牌发完了')
                return
            id_card += 1
        else:
            break
        label2['text'] = '庄家' + str(dealer_count)
        if dealer_count <= 21:
            if player_count > dealer_count:
                tkmsg.showinfo('hint', '玩家赢了')
            else:
                tkmsg.showinfo('hint', '庄家赢了')
        else:
            tkmsg.showinfo('hint', '玩家赢了')
            bt1['state'] = tk.NORMAL
            bt2['state'] = tk.DISABLED
            bt3['state'] = tk.DISABLED


win = tk.Tk()
win.title('21点扑克牌--参考自夏敏捷')
win.geometry('995x550')
dir1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image_card_21')
back = tk.PhotoImage(file=os.path.join(dir1, 'back.png'))
imgs = [tk.PhotoImage(file=os.path.join(dir1, ' ({}).png'.format(i))) for i in range(1, 53)]
deck = []
top_card = 0
dealer_ace = 0
player_ace = 0
dealer_count = 0
player_count = 0
ip_card = 0
id_card = 0
bt1 = tk.Button(win, text='发牌', width=60, height=60)
bt1.place(x=100, y=400, width=60, height=60)
bt2 = tk.Button(win, text='要牌', width=60, height=60)
bt2.place(x=200, y=400, width=60, height=60)
bt3 = tk.Button(win, text='停牌', width=60, height=60)
bt3.place(x=300, y=400, width=60, height=60)
bt1.focus_set()
bt1.bind('<ButtonPress>', callback1)
bt2.bind('<ButtonPress>', callback1)
bt3.bind('<ButtonPress>', callback1)
bt1['state'] = tk.NORMAL
bt2['state'] = tk.DISABLED
bt3['state'] = tk.DISABLED
label1 = tk.Label(win, text='玩家', width=60, height=60)
label1.place(x=0, y=300, width=60, height=60)
label2 = tk.Label(win, text='电脑', width=60, height=60)
label2.place(x=0, y=50, width=60, height=60)
list1 = [i for i in range(0, 53)]
for i in range(0, 4):
    for j in range(0, 13):
        card = Card((j + 1) + 13 * i, 0, j, i, win, imgs[i + 4 * j])
        deck.append(card)

random.shuffle(deck)
win.mainloop()
