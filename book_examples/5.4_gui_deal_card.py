#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/6/7 12:53

@author: tatatingting
"""


import tkinter as tk
import random
import os


n = 52

def gen_poker(n, pocker):
    x = 100
    while (x>0):
        x = x -1
        p1 = random.randint(0, n-1)
        p2 = random.randint(0, n-1)
        t = pocker[p1]
        pocker[p1] = pocker[p2]
        pocker[p2] = t
    return pocker


pocker = [i for i in range(n)]
pocker = gen_poker(n, pocker)
print(pocker)

(player1, player2, player3, player4) = ([], [], [], [])  # 图片列表
(p1, p2, p3, p4) = ([], [], [], [])  # 手牌编号列表

root = tk.Tk()
cv = tk.Canvas(root, bg='white', width=700, height=600)

imgs = []
for i in range(1, 5):
    for j in range(1, 14):
        imgs.insert((i-1)*13+(j-1), tk.PhotoImage(file=os.path.join('image_cards', '{}-{}.png'.format(i, j))))

for x in range(13):
    m = x * 4
    p1.append(pocker[m])
    p2.append(pocker[m+1])
    p3.append(pocker[m+2])
    p4.append(pocker[m+3])

p1.sort()  # 牌手对牌进行排序，同花色连在一起
p2.sort()
p3.sort()
p4.sort()

for x in range(0, 13):
    width_card = 20
    img = imgs[p1[x]]
    player1.append(cv.create_image((200+width_card*x, 80), image=img))
    img = imgs[p2[x]]
    player2.append(cv.create_image((100, 150+width_card*x), image=img))
    img = imgs[p3[x]]
    player3.append(cv.create_image((200 + width_card*x, 500), image=img))
    img = imgs[p4[x]]
    player4.append(cv.create_image((560, 150+width_card*x), image=img))

print('player1: ', player1)
print('player2: ', player2)
print('player3: ', player3)
print('player4: ', player4)

cv.pack()
root.mainloop()
