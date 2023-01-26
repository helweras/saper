from random import choice
import tkinter as tk


class Cell(tk.Button):
    '''Объявлен класс Cell, который является клеткой на поле'''

    def __init__(self, master=None, y=0, x=0, *args, **kwargs):
        super(Cell, self).__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.around_mines = 0  # Колличество мин вокруг клетки, колличество считается в методе count_mine класса Gamebutton
        self.mine = False  # Является ли клетка миной(True - является миной)
        self.fl_open = False  # Открыта или нет клетка на игровом поле(False - закрыта)
        self.vis = '*'

    def __repr__(self):
        return f'button {self.x} {self.y}'


class Gamebutton:
    '''Объявлен класс Gamebutton который является игровым полем и содержит основные методы
    для работы, а так же атрибуты для обязательной передачи:N - размероность поля NхN
                                                            М - колличество мин на поле'''
    win = tk.Tk()

    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.button = [[Cell(Gamebutton.win, x=j, y=i, width=3) for i in range(self.N)] for j in range(self.N)]
        self.init()
        self.count_mines()
        self.count = 0

    def init(self):
        x = 0
        while x != self.M:
            c = choice(choice(self.button))
            if c.mine:
                continue
            else:
                c.mine = True
                x += 1

    def count_mine(self, i, j):
        if not self.button[i][j].mine:
            for x in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if x not in range(0, self.N) or c not in range(0, self.N):
                        continue
                    else:
                        if self.button[x][c].mine:
                            self.button[i][j].around_mines += 1

    def count_mines(self):
        for i in range(self.N):
            for j in range(self.N):
                self.count_mine(i, j)

    def show(self):
        for i in range(self.N):
            for j in range(self.N):
                btn = self.button[i][j]
                btn.grid(row=i, column=j)

    def show_all(self):
        for i in range(self.N):
            for j in range(self.N):
                if self.button[i][j].mine:
                    print(self.button[i][j].vis, end=' ')
                else:
                    print(self.button[i][j].around_mines, end=' ')
            print()

    def start(self):
        self.show()
        self.win.mainloop()


gp = Gamebutton(10, 12)
gp.start()
gp.show_all()
