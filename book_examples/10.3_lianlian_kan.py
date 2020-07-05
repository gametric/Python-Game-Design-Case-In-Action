#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/6/21 10:20

@author: tatatingting
"""

import tkinter as tk
import random
import os
from PIL import Image, ImageTk
from tkinter import messagebox as msgbox
import threading


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def create_map():
    global map
    tamp_map = []
    m = (width * height) // 10
    print('m=', m)
    for x in range(m):
        for i in range(10):
            tamp_map.append(x)
    random.shuffle(tamp_map)
    for x in range(width):
        for y in range(height):
            map[x][y] = tamp_map[x * height + y]


def print_map():
    global image_map
    for x in range(width):
        for y in range(height):
            if map[x][y] != ' ':
                img1 = imgs[int(map[x][y])]
                id = cv.create_image((x*p_w+p_w, y*p_w+p_w), image=img1)
                image_map[x][y] = id
    cv.pack()
    for y in range(height):
        for x in range(width):
            print(map[x][y], end=' ')
        print(',', y)


def is_same(p1, p2):
    if map[p1.x][p1.y] == map[p2.x][p2.y]:
        return True
    return False


# 同行or同列
def line_check(p1, p2):
    global width, height
    abs_distance = 0
    space_count = 0
    if p1.x == p2.x or p1.y == p2.y:
        if p1.x == p2.x and p1.y != p2.y:
            if abs(p1.y-p2.y) == 1:
                print('---1-1-|| abs(1)')
                return True
            else:
                abs_distance = abs(p1.y - p2.y) - 1
                for step in range(min(p1.y, p2.y)+1, max(p1.y, p2.y)):
                    if map[p1.x][step] == ' ':
                        space_count += 1
                    else:
                        break
                if abs_distance == space_count:
                    print('---1-2-|| abs({})'.format(space_count))
                    return True
        elif p1.y == p2.y and p1.x != p2.x:
            if abs(p1.x-p2.x) == 1:
                print('---1-3- == abs(1)')
                return True
            else:
                abs_distance = abs(p1.x - p2.x) - 1
                for step in range(min(p1.x, p2.x)+1, max(p1.x, p2.x)):
                    if map[step][p1.y] == ' ':
                        space_count += 1
                    else:
                        break
                if abs_distance == space_count:
                    print('---1-4- == abs({})'.format(space_count))
                    return True
    return False


# 直角连通
def line_check2(p1, p2):
    global line_point_stack
    check_p1 = Point(p1.x, p2.y)
    check_p2 = Point(p2.x, p1.y)
    if map[check_p1.x][check_p1.y] == ' ':
        if line_check(p1, check_p1) and line_check(p2, check_p1):
            line_point_stack.append(check_p1)
            print('---2-1')
            return True
    elif map[check_p2.x][check_p2.y] == ' ':
        if line_check(p1, check_p2) and line_check(p2, check_p2):
            line_point_stack.append(check_p2)
            print('---2-2')
            return True
    return False


# 双直角连通
def line_check3(p1, p2):
    global height, width, line_point_stack
    for i in range(4):
        if i == 0:  # down
            for step in range(p1.y + 1, height):
                check_p = Point(p1.x, step)
                if map[check_p.x][check_p.y] == ' ' and line_check(p1, check_p) and line_check2(check_p, p2):
                    line_point_stack.append(check_p)
                    print('---down')
                    return True
        elif i == 1:  # up
            for step in range(0, p1.y):
                check_p = Point(p1.x, step)
                if map[check_p.x][check_p.y] == ' ' and line_check(p1, check_p) and line_check2(check_p, p2):
                    line_point_stack.append(check_p)
                    print('---up')
                    return True
        elif i == 2:  # right
            for step in range(p1.x + 1, width):
                check_p = Point(step, p1.y)
                if map[check_p.x][check_p.y] == ' ' and line_check(p1, check_p) and line_check2(check_p, p2):
                    line_point_stack.append(check_p)
                    print('---right')
                    return True
        elif i == 3:  # left
            for step in range(0, p1.x):
                check_p = Point(step, p1.y)
                if map[check_p.x][check_p.y] == ' ' and line_check(p1, check_p) and line_check2(check_p, p2):
                    line_point_stack.append(check_p)
                    print('---left')
                    return True
    if p1.x == p2.x == 0 or p1.x == p2.x == width - 1 or p1.y == p2.y == 0 or p1.y == p2.y == height - 1:
        print('--- 4.5 #')
        return True
    return False


def is_link(p1, p2):
    if line_check(p1, p2):
        return True
    elif line_check2(p1, p2):
        return True
    elif line_check3(p1, p2):
        return True
    print('no_check ~')
    return False


def draw_line(p1, p2):
    id = cv.create_line(p1.x*p_w+p_w, p1.y*p_w+p_w, p2.x*p_w+p_w, p2.y*p_w+p_w, width=5, fill='red')
    return id

def draw_link_line(p1, p2):
    global line_point_stack, line_id
    if len(line_point_stack) == 0:
        line_id.append(draw_line(p1, p2))
    if len(line_point_stack) == 1:
        z = line_point_stack[0]
        line_point_stack = []
        line_id.append(draw_line(p1, z))
        line_id.append(draw_line(p2, z))
    if len(line_point_stack) == 2:
        z1 = line_point_stack[0]
        z2 = line_point_stack[1]
        line_point_stack = []
        line_id.append(draw_line(p1, z2))
        line_id.append(draw_line(z2, z1))
        line_id.append(draw_line(z1, p2))


def undraw_connect_line():
    global line_id, map
    while len(line_id) > 0:
        for i in line_id:
            cv.delete(i)
        line_id = []
    r_map = str(map).strip()
    for sign in [' ', ',', '[', ']', "'"]:
        r_map = r_map.replace(sign, '')
    r_map = r_map.strip()
    if int(r_map) == 0:
        msgbox.showinfo(title='提示', message='恭喜！！！')


def clear_two_blocks():
    global selected_first, p1, p2, image_map
    cv.delete(selected_first_rectid)
    cv.delete(selected_second_rectid)
    map[p1.x][p1.y] = ' '
    cv.delete(image_map[p1.x][p1.y])
    map[p2.x][p2.y] = ' '
    cv.delete(image_map[p2.x][p2.y])
    selected_first = False
    undraw_connect_line()


timer_interval = 0.5
def delayrun():
    clear_two_blocks()


def callback(event):
    global selected_first, p1, p2, selected_first_rectid, selected_second_rectid
    x = (event.x-30) // int(p_w)
    y = (event.y-30) // int(p_w)
    if x > 9:
        x = 9
    if y > 9:
        y = 9
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    print(event.x-30, event.y-30, x, y)

    if map[x][y] == ' ':
        msgbox.showinfo(title='提示', message='此处无方块')
    else:
        if not selected_first:
            p1 = Point(x, y)
            selected_first_rectid = cv.create_rectangle(x*p_w+p_w*0.5, y*p_w+p_w*0.5, x*p_w+p_w*1.5, y*p_w+p_w*1.5, width=2, outline='blue')
            selected_first = True
        else:
            p2 = Point(x, y)
            if p1.x == p2.x and p1.y == p2.y:
                return
            selected_second_rectid = cv.create_rectangle(x*p_w+p_w*0.5, y*p_w+p_w*0.5, x*p_w+p_w*1.5, y*p_w+p_w*1.5, width=2, outline='yellow')
            cv.pack()
            if is_same(p1, p2) and is_link(p1, p2):
                selected_first = False
                draw_link_line(p1, p2)
                t = threading.Timer(timer_interval, delayrun)
                t.start()
            else:
                cv.delete(selected_first_rectid)
                cv.delete(selected_second_rectid)
                selected_first = False


def find2block(event):
    global selected_first_rectid, selected_second_rectid, p1, p2
    n_row = height
    n_col = width
    b_found = False
    x1, y1, x2, y2 = 0, 0, 0, 0
    for i in range(n_row*n_col):
        if b_found:
            break
        x1 = i % n_col
        y1 = i // n_col
        p1 = Point(x1, y1)
        if map[x1][y1] == ' ':
            continue
        for j in range(i+1, n_row*n_col):
            x2 = j % n_col
            y2 = j // n_col
            p2 = Point(x2, y2)
            if map[x2][y2] != ' ' and is_same(p1, p2):
                if is_link(p1, p2):
                    b_found = True
                    break
    if b_found:
        selected_first_rectid = cv.create_rectangle(x1*p_w+p_w*0.5, y1*p_w+p_w*0.5, x1*p_w+p_w*1.5, y1*p_w+p_w*1.5, width=2, outline='red')
        selected_second_rectid = cv.create_rectangle(x2*p_w+p_w*0.5, y2*p_w+p_w*0.5, x2*p_w+p_w*1.5, y2*p_w+p_w*1.5, width=2, outline='orange')
        draw_link_line(p1, p2)
        t = threading.Timer(timer_interval*2, delayrun)
        t.start()
    else:
        msgbox.showinfo(title='提示', message='没有找到合适的了！/恭喜')
    return b_found


root = tk.Tk()
root.title('PYTHON LIANLIAN KAN 连连看')

# filename = []
# for i in range(10):
#     filename.append(os.path.join('image_lianlian', str(i)+'.png'))
# imgs = [tk.PhotoImage(file=i) for i in filename]  # do not miss 'file='

imgs = []
p_w = 60
for i in range(10):
    filename = os.path.join('image_lianlian', str(i) + '.png')
    tem_img = Image.open(filename)
    tem_img = tem_img.resize((p_w, p_w))
    imgs.append(ImageTk.PhotoImage(tem_img))

selected_first = False
selected_first_rectid = -1
selected_second_rectid = -1
line_point_stack = []
line_id = []
height = 10
width = 10
map = [[' ' for y in range(height)] for x in range(width)]
image_map = [[' ' for y in range(height)] for x in range(width)]
cv = tk.Canvas(root, bg='green', width=p_w*width+p_w, height=p_w*height+p_w)
cv.bind('<Button-1>', callback)  # left
cv.bind('<Button-3>', find2block)  # right
cv.pack()
create_map()
print_map()
root.mainloop()
