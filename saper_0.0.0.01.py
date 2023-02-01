from random import choice
import tkinter as tk


class Cell(tk.Button):
    '''Объявлен класс Cell, который является клеткой на поле'''

    def __init__(self, master, x, y, *args, **kwargs):
        super(Cell, self).__init__(master, width=3, font='Calibry 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.around_mines = 0  # Колличество мин вокруг клетки, колличество считается в методе count_mine класса Gamebutton
        self.mine = False  # Является ли клетка миной(True - является миной)

    def __repr__(self):
        return f'button {self.x} {self.y}'




class Gamebutton:
    '''Объявлен класс Gamebutton который является игровым полем и содержит основные методы
    для работы, а так же атрибуты для обязательной передачи:size - размероность поля NхN
                                                            mines - колличество мин на поле'''
    win = tk.Tk()
    size = 10

    def __init__(self, mines):
        self.mines = mines
        self.button = []
        for i in range(self.size):
            tmp = []
            for j in range(self.size):
                btn = Cell(Gamebutton.win, x=i, y=j)
                btn.config(command=lambda button=btn: self.click_button(button))
                tmp.append(btn)
            self.button.append(tmp)

        self.count = 0

    def click_button(self, clicked_cell: Cell):
        if clicked_cell.mine:
            clicked_cell.config(text='x', state=tk.DISABLED, background='red')
        else:
            clicked_cell.config(text=clicked_cell.around_mines, state=tk.DISABLED, background='blue')

            # clicked_cell.config(text=clicked_cell.around_mines, state=tk.DISABLED, background='blue')

    def place_mines(self):
        x = 0
        while x != self.mines:
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
                    if x not in range(0, self.size) or c not in range(0, self.size):
                        continue
                    else:
                        if self.button[x][c].mine:
                            self.button[i][j].around_mines += 1

    def count_mines(self):
        for i in range(self.size):
            for j in range(self.size):
                self.count_mine(i, j)

    def show(self):
        for i in range(self.size):
            for j in range(self.size):
                btn = self.button[i][j]
                btn.grid(row=i, column=j)

    def show_all(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.button[i][j].mine:
                    print('*', end=' ')
                else:
                    print(self.button[i][j].around_mines, end=' ')
            print()

    def start(self):
        self.place_mines()
        self.count_mines()
        self.show()
        self.show_all()
        self.win.mainloop()


gp = Gamebutton(10)
gp.start()
