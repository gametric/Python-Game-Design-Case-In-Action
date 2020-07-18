#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/7/8 11:51

@author: tatatingting
"""


import os
import tkinter as tk
import random
from threading import Timer
import time
import operator
import winsound
from tkinter import messagebox as tkmsg
import numpy as np


def on_btn_get_click():
    global k, players_card, my_turn
    if k == 136:
        tkmsg.showinfo(title='提示', message='牌摸完啦~')
        out_btn['state'] = tk.NORMAL
        chi_btn['state'] = tk.DISABLED
        peng_btn['state'] = tk.DISABLED
        get_btn['state'] = tk.DISABLED
        my_turn = True
        return
    m_aCards[k].move_to(90+55*13, my_height)
    m_aCards[k].set_front(True)
    players_card[0].append(m_aCards[k])
    # m_aCards[k].bind('<ButtonPress>', btn_mouse_down)
    sort_poker(players_card[0])
    result = computer_card_num(players_card[0])
    if result:
        win_btn['state'] = tk.NORMAL
        tkmsg.showinfo(title='恭喜', message='玩家Win!')
        return
    k += 1
    out_btn['state'] = tk.NORMAL
    chi_btn['state'] = tk.DISABLED
    peng_btn['state'] = tk.DISABLED
    get_btn['state'] = tk.DISABLED
    my_turn = True


def computer_selected_card(a, ntype, nnum):
    for i in range(len(a)):
        card = a[i]
        if card.m_ntype==ntype and card.m_nnum==nnum:
            return i
    return -1


def computer_card(cards):
    pair_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for i in range(14):
        card = cards[i]
        if card.imageID>10 and card.imageID<20:
            pair_array[0][0] += 1
            pair_array[0][card.imageID-10] += 1
        if card.imageID>20 and card.imageID<30:
            pair_array[0][1] += 1
            pair_array[0][card.imageID - 20] += 1
        if card.imageID>30 and card.imageID<40:
            pair_array[2][0] += 1
            pair_array[2][card.imageID - 30] += 1
        if card.imageID>40 and card.imageID<50:
            pair_array[3][0] += 1
            pair_array[3][card.imageID - 40] += 1
    print(pair_array)
    for j in range(1, 10):
        if pair_array[3][j] == 1:
            k = computer_selected_card(cards, 3+1, j)
            return k
    for i in range(3):
        for j in range(1, 10):
            if pair_array[i][j] >= 3:
                pair_array[i][j] -= 3
            if j<=7 and pair_array[i][j]>=1 and pair_array[i][j+1]>=1 and pair_array[i][j+2]>=1:
                pair_array[i][j] -= 1
                pair_array[i][j+1] -= 1
                pair_array[i][j+2] -= 1
    for i in range(3, -1):
        for j in range(1, 10):
            if pair_array[i][j] == 2:
                k = computer_selected_card(cards, i+1, j)
                return k
    k = random.randint(0, 13)
    return k


def computer_out():
    global k, my_turn
    if k == 136:
        tkmsg.showinfo(title='提示', message='牌摸完啦~')
        out_btn['state'] = tk.NORMAL
        chi_btn['state'] = tk.DISABLED
        peng_btn['state'] = tk.DISABLED
        get_btn['state'] = tk.DISABLED
        my_turn = True
        return
    m_aCards[k].move_to(90+55*13, pc_height)
    m_aCards[k].set_front(True)
    players_card[1].append(m_aCards[k])
    result = computer_card_num(players_card[1])
    if result:
        tkmsg.showinfo(title='遗憾', message='电脑Win!')
        return
    i = computer_card(players_card[1])
    card = players_card[1][i]
    del(players_card[1][i])
    players_card_out[1].append(card)
    card.set_front(True)
    sort_poker(players_card[1])
    card.x = len(players_card_out[1])*25-25
    card.y = pc_height+175
    card.move_to(card.x, card.y)
    k += 1
    my_turn = True


def can_peng(a, card):
    n = 0
    for i in range(len(a)):
        c = a[i]
        if c.imageID == card.imageID:
            n += 1
    if n >= 2:
        return True
    print('不能碰牌！', card.imageID)
    return False


def can_chi(a, card):
    n = 0
    if card.m_ntype == 4:
        return False
    for i in range(len(a) - 1):
        c1 = a[i]
        c2 = a[i+1]
        if c1.m_nnum == card.m_nnum + 1 and c1.m_ntype == card.m_ntype and c2.m_nnum == card.m_nnum + 2 and c2.m_ntype == card.m_ntype:
            return True
        if c1.m_nnum == card.m_nnum - 1 and c1.m_ntype == card.m_ntype and c2.m_nnum == card.m_nnum + 1 and c2.m_ntype == card.m_ntype:
            return True
        if c1.m_nnum == card.m_nnum - 2 and c1.m_ntype == card.m_ntype and c2.m_nnum == card.m_nnum - 1 and c2.m_ntype == card.m_ntype:
            return True
    print('不能吃牌！', card.imageID)
    return False


def fun_players_logic():
    my_turn = True
    get_btn['state'] = tk.NORMAL
    if len(players_card_out[1]) > 0:
        card = players_card_out[1][len(players_card_out[1]) - 1]
        if can_peng(players_card[0], card):
            peng_btn['state'] = tk.NORMAL
        elif can_chi(players_card[0], card):
            chi_btn['state'] = tk.NORMAL
        else:
            peng_btn['state'] = tk.DISABLED
            chi_btn['state'] = tk.DISABLED
    else:
        get_btn['state'] = tk.NORMAL


def on_btn_out_click():
    global my_turn, players_selectcard, players_card_out, m_lastcard,players_card
    print('出牌')
    if not my_turn:
        return
    if players_selectcard == None:
        tkmsg.showinfo(title='提示', message='还没选择出的牌')
        return
    print(players_selectcard)
    if not(players_selectcard == None):
        out_btn['state'] = tk.DISABLED
        players_card_out[0].append(players_selectcard)
        players_selectcard.x = len(players_card_out[0])*25-25
        players_selectcard.y = my_height-175
        players_selectcard.move_to(players_selectcard.x, players_selectcard.y)
        print(players_selectcard.cardID)
        del(players_card[0][players_selectcard.cardID])
        m_lastcard = None
        players_selectcard = None
        my_turn = False
        out_btn['state'] = tk.DISABLED
        sort_poker(players_card[0])
        computer_out()
        fun_players_logic()


class hu_main():
    def __init__(self):
        self.all_pai = [[6, 1, 4, 1, 0, 0, 0, 0, 0, 0],
                        [3, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [5, 2, 3, 0, 0, 0, 0, 0, 0, 0]]
        if self.win(self.all_pai):
            print('Hu!\n')
        else:
            print('Not Hu!\n')
    def win(self, all_pai):
        jiang_pos = 0
        jiang_existed = False
        for i in range(4):
            yushu = all_pai[i][0]%3
            if yushu == 1:
                return False
            if yushu == 2:
                if jiang_existed == True:
                    return False
                jiang_pos = i
                jiang_existed = True
        for i in range(4):
            if i != jiang_pos:
                if not self.analyze(all_pai[i], i==3):
                    return False
        success = False
        for j in range(1, 10):
            if all_pai[jiang_pos][j] >=2:
                all_pai[jiang_pos][j] -= 2
                all_pai[jiang_pos][0] -= 2
            if self.analyze(all_pai[i], i==3):
                success = True
            all_pai[jiang_pos][j] += 2
            all_pai[jiang_pos][0] += 2
            if success == True:
                break
        return success
    def analyze(self, akindpai, zipai):
        if akindpai[0] == 0:
            return True
        for j in range(1, 10):
            if akindpai[j] != 0:
                break
        if akindpai[j] >= 3:
            akindpai[j] -= 3
            akindpai[0] -= 3
            result = self.analyze(akindpai, zipai)
            akindpai[j] += 3
            akindpai[0] += 3
            return False
        if (not zipai) and (j<8) and (akindpai[j+1]>0) and (akindpai[j+2]>0):
            akindpai[j] -= 1
            akindpai[j+1] -= 1
            akindpai[j+2] -= 1
            akindpai[0] -= 3
            result = self.analyze(akindpai, zipai)
            akindpai[j] += 1
            akindpai[j+1] += 1
            akindpai[j+2] += 1
            akindpai[0] += 3
        return False


def computer_card_num(cards):
    pair_array = np.zeros((4, 10))
    print('玩家手中的牌： ', len(cards))
    for i in range(14):
        card = cards[i]
        if card.imageID>10 and card.imageID<20:
            pair_array[0][0] += 1
            pair_array[0][card.imageID-10] += 1
        if card.imageID>20 and card.imageID<30:
            pair_array[1][0] += 1
            pair_array[1][card.imageID-20] += 1
        if card.imageID>30 and card.imageID<40:
            pair_array[2][0] += 1
            pair_array[2][card.imageID-30] += 1
        if card.imageID>40 and card.imageID<50:
            pair_array[3][0] += 1
            pair_array[3][card.imageID-40] += 1
    print(pair_array)
    hu = hu_main()
    result = hu.win(pair_array)
    return result


def on_btn_chi_click():
    global my_turn
    card = players_card_out[1][len(players_card_out[1])-1]
    card.move_to(90+50*13, my_height)
    card.set_front(True)
    players_card[0].append(card)
    print('碰吃的牌： ', card.imageID)
    sort_poker(players_card[0])
    result = computer_card_num(players_card[0])
    if result:
        win_btn['state'] = tk.NORMAL
        out_btn['state'] = tk.DISABLED
        tkmsg.showinfo(title='恭喜', message='玩家Win!')
        return
    out_btn['state'] = tk.NORMAL
    chi_btn['state'] = tk.DISABLED
    peng_btn['state'] = tk.DISABLED
    get_btn['state'] = tk.DISABLED
    my_turn = True


def btn_mouse_down(event):
    global m_lastcard, players_selectcard
    if event.widget['state'] == tk.DISABLED:
        return
    if not event.widget.m_bfront:
        return
    card = event.widget
    card.y -= 20
    card.place(x=event.widget.x, y=event.widget.y)
    if not m_lastcard:
        m_lastcard = card
        players_selectcard = card
    else:
        m_lastcard.move_to(m_lastcard.get_x(), m_lastcard.get_y()+20)
        m_lastcard = card
        players_selectcard = card


class Card(tk.Button):
    def __init__(self, m_ntype, num, bm, master):
        tk.Button.__init__(self, master)
        # m_ntype: 1=饼，2=条，3=万，4=字牌
        self.m_ntype = m_ntype
        self.m_nnum = num
        self.img = bm
        self.imageID = self.m_ntype*10 + self.m_nnum
        # front_url = os.path.join('image_majiang', '{}.png'.format(str(self.imageID)))
        self['width'] = 84
        self['height'] = 117
        self['text'] = '{}.png'.format(str(self.imageID))
        self.set_front(False)
        self.bind('<ButtonPress>', btn_mouse_down)
        self.cardId = 0
    # def __cmp__(self, other):
        # return cmp(self.imageID, other.imageID)
    def set_front(self, b):
        self.m_bfront = b
        if b:
            self['image'] = self.img
        else:
            self['image'] = back
    def move_to(self, x1, y1):
        self.place(x=x1, y=y1)
        self.x = x1
        self.y = y1
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_imageID(self):
        return self.imageID


def load_cards():
    for m_ntype in range(1, 4):
        for num in range(1, 10):
            front_url = os.path.join('image_majiang', '{}.png'.format(str(m_ntype*10 + num)))
            imgs.append(tk.PhotoImage(file=front_url))
            for n in range(4):
                card = Card(m_ntype, num, imgs[len(imgs)-1], win)
                m_aCards.append(card)
    m_ntype = 4
    for num in range(1, 8):
        front_url = os.path.join('image_majiang', '{}.png'.format(str(m_ntype*10 + num)))
        imgs.append(tk.PhotoImage(file=front_url))
        for n in range(4):
            card = Card(m_ntype, num, imgs[len(imgs) - 1], win)
            m_aCards.append(card)


def shift(k):
    i = k % 2
    j = (k-k%2)/2
    if i == 0:
        m_aCards[k].set_front(True)
        m_aCards[k].move_to(80+80*j, my_height)
        # m_aCards[k].bind('<ButtonPress>', btn_mouse_down)
    elif i == 1:
        m_aCards[k].set_front(True)
        m_aCards[k].move_to(80+80*j, pc_height)
    players_card[i].append(m_aCards[k])


def sort_poker(cards):
    n = len(cards)
    cards.sort(key=operator.attrgetter('imageID'))
    print('排序后', end=': ')
    for index in range(n):
        print(cards[index].imageID, end=', ')
        new_x = 80 + 80 * index
        y = cards[index].get_y()
        cards[index].move_to(new_x, y)
        cards[index].cardID = index


def shift_cards():
    global k
    for k in range(26):
        shift(k)
    print('\n玩家-按花色理牌', end=' ')
    sort_poker(players_card[0])
    print('\n电脑-按花色理牌', end=' ')
    sort_poker(players_card[1])
    # out_player_num = 0
    k = 26


def reset_game():
    # players_card[0] = []
    # players_card[1] = []
    for n in range(len(m_aCards)):
        m_aCards[n].x = 90+30*(n%34)
        m_aCards[n].y = pc_height+150+50*(n-n%34)/34
        m_aCards[n].move_to(m_aCards[n].x, m_aCards[n].y)
        # m_aCards[n].set_front(False)
    shift_cards()
    # m_lastcard = None
    # players_card_out[0] = []
    # players_card_out[1] = []


def begin_game():
    # my_turn = True
    load_cards()
    random.shuffle(m_aCards)
    reset_game()



win = tk.Tk()
win.title('两人麻将 -- 练习项目（精简版），参考自夏敏捷')
win.geometry('1250x750')
imgs = []
back = tk.PhotoImage(os.path.join('image_majiang', 'back.png'))
m_aCards = []
players_card = [[], []]
players_card_out = [[], []]
k = 0
m_lastcard = None
players_selectcard = None
my_turn = True

chi_btn = tk.Button(win, text='吃牌', command=on_btn_chi_click)
peng_btn = tk.Button(win, text='碰牌', command=on_btn_chi_click)
out_btn = tk.Button(win, text='出牌', command=on_btn_out_click)
get_btn = tk.Button(win, text='摸牌', command=on_btn_get_click)
win_btn = tk.Button(win, text='和牌', width=70, height=30)

btn_x = 500
btn_y = 700
my_height = 550
pc_height = 50
chi_btn.place(x=btn_x+100, y=btn_y, width=70, height=40)
peng_btn.place(x=btn_x+200, y=btn_y, width=70, height=40)
out_btn.place(x=btn_x+300, y=btn_y, width=70, height=40)
get_btn.place(x=btn_x+400, y=btn_y, width=70, height=40)
win_btn.place(x=btn_x, y=btn_y, width=70, height=40)

# get_btn.pack_forget()

chi_btn['state'] = tk.DISABLED
peng_btn['state'] = tk.DISABLED
out_btn['state'] = tk.DISABLED
# get_btn['state'] = tk.DISABLED
win_btn['state'] = tk.DISABLED

begin_game()
win.mainloop()
