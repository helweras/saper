from random import choice
import tkinter as tk


class Cell(tk.Button):
    '''Объявлен класс Cell, который является клеткой на поле'''
    open_cell = False
    colors = {0: '#8A2BE2', 1: '#0000FF', 2: '#008000', 3: '#E30205', 4: '#090B5D', 5: '#5C3624', 6: '#30D5C8',
              7: '#050506',
              8: '#C5D0E6'}

    def __init__(self, master, x, y, *args, **kwargs):
        super(Cell, self).__init__(master, width=3, font='Calibry 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.around_mines = 0  # Колличество мин вокруг клетки, колличество считается в методе count_mine класса Gamebutton
        self.mine = False  # Является ли клетка миной(True - является миной)

    def round_cell(self, board):
        if self.open_cell and self.around_mines == 0:
            for i in range(self.x - 1, self.x + 2):
                for j in range(self.y - 1, self.y + 2):
                    if i not in range(0, len(board)) or j not in range(0, len(board)):
                        continue
                    else:
                        board[i][j].open_cell = True
                        board[i][j].config(text=board[i][j].around_mines, state=tk.DISABLED, background='white',
                                           disabledforeground=self.colors[board[i][j].around_mines])

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
                btn.config(command=lambda button=btn: self.click_button(button), disabledforeground='black')
                tmp.append(btn)
            self.button.append(tmp)

        self.count = 0

    def click_button(self, clicked_cell: Cell):
        if clicked_cell.mine:
            clicked_cell.config(text='x', state=tk.DISABLED, background='red')
            clicked_cell.open_cell = True
        else:
            # clicked_cell.config(text=clicked_cell.around_mines, state=tk.DISABLED, background='white',
            #                     disabledforeground=clicked_cell.colors[clicked_cell.around_mines])
            clicked_cell.open_cell = True
            # clicked_cell.round_cell(self.button)
            self.open_around(clicked_cell)
            print(repr(self.button[clicked_cell.x][clicked_cell.y].open_cell))
        clicked_cell.config(relief=tk.SUNKEN)

    def open_around(self, cell: Cell):
        list_Cell = [cell]
        while list_Cell:

            but = list_Cell.pop()
            if but.around_mines:
                but.open_cell = True
                but.config(text=but.around_mines, disabledforeground=but.colors[but.around_mines], state=tk.DISABLED)
            else:
                but.open_cell = True
                but.config(text='', state=tk.DISABLED)
            if not but.around_mines:
                x, y = but.x, but.y
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2):
                        if i not in range(0, len(self.button)) or j not in range(0, len(self.button)):
                            continue
                        else:
                            if self.button[i][j] not in list_Cell and self.button[i][j].open_cell is False:
                                list_Cell.append(self.button[i][j])
            but.config(relief=tk.SUNKEN)


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
