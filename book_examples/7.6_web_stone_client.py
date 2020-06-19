#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/6/15 14:06

@author: tatatingting
"""


import tkinter as tk
from tkinter import messagebox as msgbox
import socket
import threading
import os


def drawQiPan():
    for i in range(0, 15):
        cv.create_line(
            20,
            20 + 40 * i,
            580,
            20 + 40 * i,
            width=2,
        )
    for i in range(0, 15):
        cv.create_line(
            20 + 40 * i,
            20,
            20 + 40 * i,
            580,
            width=2,
        )
    cv.pack()


def sendMessage(pos):
    global s
    s.sendto(pos.encode(), (host, port))
    print('客户端发送信息', pos)


def win_lose():
    a = str(turn)
    print('a=', a)
    for i in range(0, 11):
        for j in range(0, 11):
            if map[i][j] == a and map[i+1][j+1] == a and map[i+2][j+2] == a and map[i+3][j+3] == a and map[i+4][j+4] == a:
                print('x = y 轴上形成五子连珠')
                return True
    for i in range(4, 15):
        for j in range(0, 11):
            if map[i][j] == a and map[i-1][j+1] == a and map[i-2][j+2] == a and map[i-3][j+3] == a and map[i-4][j+4] == a:
                print('x = -y 轴上形成五子连珠')
                return True
    for i in range(0, 15):
        for j in range(4, 15):
            if map[i][j] == a and map[i][j-1] == a and map[i][j-2] == a and map[i][j-3] == a and map[i][j-4] == a:
                print('y 轴上形成五子连珠')
                return True
    for i in range(0, 11):
        for j in range(0, 15):
            if map[i][j] == a and map[i+1][j] == a and map[i+2][j] == a and map[i+3][j] == a and map[i+4][j] == a:
                print('x 轴上形成五子连珠')
                return True
    return False


def callback(event):
    global turn
    global Myturn

    if Myturn == -1:
        Myturn = turn
    else:
        if (Myturn != turn):
            msgbox.showinfo(title='提示', message='还没轮到自己走棋')
            return
    # print('clicked at ', event.x, event.y, turn)

    x = (event.x) // 40  # 610x610, 15x15
    y = (event.y) // 40
    print('clicked at ', x, y, turn)

    if map[x][y] != ' ':
        msgbox.showinfo(title='提示', message='已有棋子')
    else:
        img1 = imgs[turn]
        cv.create_image((x*40+20, y*40+20), image=img1)
        cv.pack()

        map[x][y] = str(turn)

        pos = str(x) + ',' + str(y)
        sendMessage('move|' + pos)
        print('客户端走棋的位置', pos)
        label1['text'] = '客户端走棋的位置' + pos

        # 输赢信息
        if win_lose() == True:
            if turn == 0:
                msgbox.showinfo(title='提示', message='黑方赢了')
                sendMessage('over|黑方赢了')
            else:
                msgbox.showinfo(title='提示', message='白方赢了')
                sendMessage('over|白方赢了')

        # 换对手走棋
        if turn == 0:
            turn = 1
        else:
            turn = 0

    return None



def callexit(event):
    pos = 'exit|'
    sendMessage(pos)
    os._exit(0)


def print_map():
    for j in range(0, 15):
        for i in range(0, 15):
            print(map[i][j], end=' ')
        print('w')


def drawOtherChess(x, y):
    global turn
    img1 = imgs[turn]
    cv.create_image((x * 40 + 20, y * 40 + 20), image=img1)
    cv.pack()
    map[x][y] = str(turn)
    if turn == 0:
        turn = 1
    else:
        turn = 0


def receiveMessage():
    global s
    while True:
        global addr
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        a = data.split('|')
        print('................客户端正在接收消息...')

        if not data:
            print('server has exited!')
            break
        # elif a[0] == 'join':
        #     print('client 连接服务器！')
        #     label1['text'] = 'client 连接服务器成功，请你走棋！'
        elif a[0] == 'exit':
            print('client 对方退出！')
            label1['text'] = 'server 对方退出，游戏结束！'
        elif a[0] == 'over':
            print_map()
            label1['text'] = data.split('|')[0]
            msgbox.showinfo(title='提示', message=data.split('|')[1])
        elif a[0] == 'move':
            print('received:  ', data, 'from ', addr)
            p = a[1].split(',')
            x = int(p[0])
            y = int(p[1])
            print(p[0], p[1])
            label1['text'] = '服务器走的位置' + p[0] + p[1]
            drawOtherChess(x, y)
    s.close()


def startNewThread():
    thread = threading.Thread(target=receiveMessage, args=())
    thread.setDaemon(True)
    thread.start()
    print('thread start')


if __name__ == '__main__':
    root = tk.Tk()
    root.title('网络五子棋v1.0--UDP 客户端')
    imgs = [
        tk.PhotoImage(file=os.path.join('image_stone', 'stone_black.PNG')),
        tk.PhotoImage(file=os.path.join('image_stone', 'stone_white.PNG')),
    ]
    turn = 0
    Myturn = -1

    map = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] for y in range(15)]

    cv = tk.Canvas(root, bg='green', width=610, height=610)
    drawQiPan()
    cv.bind('<Button-1>', callback)
    cv.pack()

    label1 = tk.Label(root, text="客户端....")
    label1.pack()

    button1 = tk.Button(root, text='退出游戏')
    button1.bind('<Button-1>', callexit)
    button1.pack()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('................客户端正在尝试通信...')

    port = 8000
    host = 'localhost'  # 192.168.0.101

    pos = 'join|'  # 连接服务器
    sendMessage(pos)

    startNewThread()
    root.mainloop()
