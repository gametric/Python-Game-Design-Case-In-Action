#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2020/7/16 11:08

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


class Grid(object):
    def __init__(self, master=None, window_width=1000, window_height=600, grid_width=50, offset=10):
        self.width = window_width
        self.height = window_height
        self.grid_width = grid_width
        self.offset = offset
        self.grid_x = self.width // self.grid_width
        self.grid_y = self.height // self.grid_width
        self.bg = '#EBEBEB'
        self.canvas = tk.Canvas(master, width=self.width + 2 * self.offset, height=self.height + 2 * self.offset,
                                bg=self.bg)
        self.canvas.pack()
        self.grid_list = self.get_grid_list()

    def draw(self, pos, color):
        x = pos[0] * self.grid_width + self.offset
        y = pos[1] * self.grid_width + self.offset
        self.canvas.create_rectangle(x, y, x + self.grid_width, y + self.grid_width, fill=color, outline=color)

    def get_grid_list(self):
        grid_list = []
        for y in range(self.grid_y):
            for x in range(self.grid_x):
                grid_list.append((x, y))
        return grid_list


class Food(object):
    def __init__(self, Grid):
        self.grid = Grid
        self.color = '#23D978'
        self.set_pos()

    def set_pos(self):
        x = random.randint(0, self.grid.grid_x - 1)
        y = random.randint(0, self.grid.grid_y - 1)
        self.pos = (x, y)

    def display(self):
        self.grid.draw(self.pos, self.color)


class Snake(object):
    def __init__(self, Grid):
        self.grid = Grid
        self.body = [(10, 6), (10, 7), (10, 8), (10, 9), (10, 10)]
        self.direction = 'Up'
        self.status = ['run', 'stop']
        self.speed = 300
        self.color = '#5FA8D9'
        self.game_over = False
        self.hit = False

    def available_grid(self):
        return [i for i in self.grid.grid_list if i not in self.body[1:]]

    def change_direction(self, direction):
        self.direction = direction

    def display(self):
        for (x, y) in self.body:
            self.grid.draw((x, y), self.color)

    def move(self, food):
        head = self.body[0]
        if self.direction == 'Up':
            new = (head[0], head[1] - 1)
        elif self.direction == 'Down':
            new = (head[0], head[1] + 1)
        elif self.direction == 'Left':
            new = (head[0] - 1, head[1])
        else:
            new = (head[0] + 1, head[1])
        if not (food.pos == head):
            pop = self.body.pop()
            self.grid.draw(pop, self.grid.bg)
        else:
            self.hit = True
        self.body.insert(0, new)
        if not (new in self.available_grid()):
            self.status.reverse()
            self.game_over = True
        else:
            self.grid.draw(new, self.color)


class SnakeGame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.grid = Grid(master=master)
        self.snake = Snake(self.grid)
        self.food = Food(self.grid)
        self.display_food()
        self.bind_all('<KeyRelease>', self.key_release)
        self.snake.display()
        self.score = 0
        self.score_store = [0, 0]
        self.score_lab = tk.Label(self.master)
        self.score_lab.pack()
        self.flag = True

    def display_food(self):
        while self.food.pos in self.snake.body:
            self.food.set_pos()
        self.food.display()

    def run(self):
        self.score_lab.config(self.score_lab, text="Now your score is < {} >, the last player's score is {} .".format(self.score, self.score_store[-2]))
        if not self.snake.status[0] == 'stop':
            self.snake.move(self.food)
            if self.snake.hit:
                self.display_food()
                self.score += 1
                self.snake.hit = False
        if self.snake.game_over:
            # message = tkmsg.showinfo('Game Over', 'the bigger score is: %d' % max(self.score, self.score_store[-2])
            # if message == 'ok':
            #     sys.exit()
            self.game_again()
        self.after(self.snake.speed, self.run)

    def key_release(self, event):
        key = event.keysym
        key_dict = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if key in key_dict.keys() and not (key == key_dict[self.snake.direction]):
            self.snake.change_direction(key)
            self.snake.move(self.food)
        elif key == 'p':
            self.snake.status.reverse()

    def game_again(self):
        self.snake.status.reverse()
        self.score_store.append(self.score)
        self.score = 0
        # self.grid.bg = '#EBEBEB'
        if self.flag:
            for i in range(self.grid.grid_x):
                for j in range(self.grid.grid_y):
                    self.grid.draw((i, j), '#992222')
            self.flag = False
            for (x, y) in self.snake.body:
                self.grid.draw((x, y), self.grid.bg)
            self.snake = Snake(self.grid)
            self.snake.color = '#' + str(random.randint(100000, 999999))
            self.snake.display()
            self.display_food()
            self.snake.speed = 1
        else:
            for i in range(self.grid.grid_x):
                for j in range(self.grid.grid_y):
                    self.grid.draw((i, j), self.grid.bg)
            self.flag = True
            for (x, y) in self.snake.body:
                self.grid.draw((x, y), self.grid.bg)
            self.snake = Snake(self.grid)
            self.snake.color = '#' + str(random.randint(100000, 999999))
            self.snake.display()
            self.display_food()
            self.snake.speed = 300


if __name__ == '__main__':
    root = tk.Tk()
    root.title('贪吃蛇~~~（多人游戏版本-分数比拼）')
    snake_game = SnakeGame(root)
    snake_game.run()
    snake_game.mainloop()
