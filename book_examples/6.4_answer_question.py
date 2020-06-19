#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/6/7 15:50

@author: tatatingting
"""

import sqlite3  # 导入SQLite

if 1:
    # 连接SQLite数据库，数据库文件是test2.db，如果文件不存在，则会自动在当前目录创建
    conn = sqlite3.connect('test2.db')
    cursor = conn.cursor()
    # 执行一条SQL语句，创建exam表
    cursor.execute(
        'CREATE TABLE [exam]([question] VARCHAR(80) NULL, [Answer_A] VARCHAR(1) NULL, [Answer_B] VARCHAR(1) NULL, '
        '[Answer_C] VARCHAR(1) NULL, [Answer_D] VARCHAR(1) NULL, [right_Answer] VARCHAR(1) NULL)')

    QUESTIONS_AND_ANSWERS = [
        ('哈雷彗星的平均周期为', '54年', '56年', '73年', '83年', 'C'),
        ('夜郎自大中“夜郎”指的是现在哪个地方？', '贵州', '云南', '广西', '福建', 'A'),
        ('在中国历史上是谁发明了麻药', '孙思邈', '华佗', '张仲景', '扁鹊', 'B'),
        ('京剧中的花旦是指', '年轻男子', '年轻女子', '年长男子', '年长女子', 'B'),
        ('在天愿做比翼鸟，在地愿为连理枝，讲述的是谁的爱情故事？', '焦仲卿和刘兰芝', '梁山伯与祝英台', '崔莺莺和张生', '杨贵妃和唐明皇', 'D'),
    ]

    for question_and_answer in QUESTIONS_AND_ANSWERS:
        cursor.execute(
            "insert into exam (question, Answer_A, Answer_B, Answer_C, Answer_D, right_Answer) values (?, ?, ?, ?, ?, ?)",
            question_and_answer)

    print(cursor.rowcount)
    cursor.close()
    conn.commit()  # 提交事务
    conn.close()

# 读取试题
conn = sqlite3.connect('test2.db')
cursor = conn.cursor()
cursor.execute('select * from exam')
values = cursor.fetchall()
cursor.close()
conn.close()

# gui
import tkinter as tk


def show_info(vText):
    show_info_label.config(show_info_label, text=vText)


def callNext():
    global k
    global score
    user_answer = r.get()
    print(r.get(), k)

    if k >= len(values) - 1:
        show_info("题目做完了！正确答案是： " + str(values[k][0]) + ": " + str(values[k][5]))
        return

    if user_answer == values[k][5]:
        show_info("恭喜o(*￣▽￣*)ブ你答对了！正确答案是： " + str(values[k][0]) + ": " + str(values[k][5]))
        score += 10
    else:
        show_info("遗憾( ▼-▼ )你答错了！正确答案是： " + str(values[k][0]) + ": " + str(values[k][5]))

    k += 1

    timu["text"] = values[k][0]
    radio1["text"] = values[k][1]
    radio2["text"] = values[k][2]
    radio3["text"] = values[k][3]
    radio4["text"] = values[k][4]

    r.set('E')


def callResult():
    show_info("你的得分： " + str(score))


root = tk.Tk()
root.title("Python智力问答游戏")
root.geometry("500x200")

r = tk.StringVar()
r.set('E')  # 初始值为E，表示没选中
k = 0
score = 0
timu = tk.Label(root, text=values[k][0])
timu.pack()

f1 = tk.Frame(root)
f1.pack()

radio1 = tk.Radiobutton(f1, variable=r, value='A', text=values[k][1])
radio1.pack()
radio2 = tk.Radiobutton(f1, variable=r, value='B', text=values[k][2])
radio2.pack()
radio3 = tk.Radiobutton(f1, variable=r, value='C', text=values[k][3])
radio3.pack()
radio4 = tk.Radiobutton(f1, variable=r, value='D', text=values[k][4])
radio4.pack()

f2 = tk.Frame(root)
f2.pack()

tk.Button(f2, text="下一题", command=callNext).pack(side="left")
tk.Button(f2, text="结 果", command=callResult).pack(side="left")

show_info_label = tk.Label(root)  # 提示标签
show_info_label.pack()

root.mainloop()
