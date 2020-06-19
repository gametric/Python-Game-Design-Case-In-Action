#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/6/6 21:37

@author: tatatingting
"""

# Word Jumble 猜单词游戏

import random

WORDS = ("python", "juice", "easy", "difficult", "answer", "continue", "phone", "hello", "pose", "game")

print(
    """
        欢迎参加猜单词游戏
    把字母组合成一个正确的单词。
"""
)

is_continue = 'y'
while is_continue == 'y' or is_continue == 'Y':  # 循环
    word = random.choice(WORDS)
    correct = word
    jumble = ""
    while word:
        position = random.randrange(len(word))
        jumble += word[position]
        word = word[:position] + word[(position + 1):]
    print("乱序后的单词：", jumble)

    guess = input("\n请你猜： ")
    while guess != correct and guess != '' and guess != '886':
        if guess == '666':
            print("提示信息： 单词的第一个字母是", correct[0])
        else:
            print("对不起，不正确。（放弃请输入：886，获取提示请输入：666）")
            print("乱序后的单词：", jumble)
        guess = input("继续猜： ")

    if guess == correct:
        print("真棒，你猜对了！")
    is_continue = input("\n是否继续（Y/N): ")

print(
    """
        感谢光顾本游戏！
            再会！
        开心每一天^-^
"""
)
