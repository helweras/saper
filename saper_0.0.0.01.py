from random import choice
import tkinter as tk
from tkinter.messagebox import showinfo


class Cell(tk.Button):
    '''Объявлен класс Cell, который является клеткой на поле'''
    open_cell = False
    colors = {0: '#8A2BE2', 1: '#0000FF', 2: '#008000', 3: '#E30205', 4: '#090B5D', 5: '#5C3624', 6: '#30D5C8',
              7: '#050506',
              8: '#C5D0E6', 9: 'red'}

    def __init__(self, master, x, y, *args, **kwargs):
        super(Cell, self).__init__(master, width=3, font='Calibry 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.around_mines = 0  # Кол-во мин вокруг клетки, колличество считается в методе count_mine класса Gamebutton
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


class Gamebutton:
    '''Объявлен класс Gamebutton который является игровым полем и содержит основные методы
    для работы, а так же атрибуты для обязательной передачи:size - размероность поля NхN
                                                            mines - колличество мин на поле'''
    win = tk.Tk()
    GAME_OVER = False
    found_mines = 0

    def __init__(self, mines=10, size=10):
        self.mines = mines
        self.size = size
        self.button = []
        self.free_islam = mines
        for i in range(self.size):
            tmp = []
            for j in range(self.size):
                btn = Cell(Gamebutton.win, x=i, y=j)
                btn.config(command=lambda button=btn: self.click_button(button), disabledforeground='black',
                           background='white')
                btn.bind('<Button-3>', self.right_click)
                tmp.append(btn)
            self.button.append(tmp)

        self.count = 0

    def right_click(self, event):
        get_event = event.widget

        def state():
            """Функция для сокращения строк кода.
            Описывает поведения кнопки при нажатии пкм когда на ней стоит знак шахида"""
            get_event.open_cell = False
            get_event['state'] = 'normal'
            get_event['text'] = ''
            self.free_islam += 1
            if get_event.mine:
                self.found_mines -= 1

        if self.free_islam > 0:
            if get_event['state'] == 'normal':
                get_event['state'] = 'disabled'
                get_event['disabledforeground'] = 'red'
                get_event['text'] = '☪'
                get_event.open_cell = True
                self.free_islam -= 1
                if get_event.mine:
                    self.found_mines += 1
            elif get_event['text'] == '☪':
                state()
        elif self.free_islam == 0 and get_event['text'] == '☪':
            state()

    def click_button(self, clicked_cell: Cell):
        if clicked_cell.mine:
            self.open_all()
            showinfo('Game over', 'Саня - лох')
        else:
            clicked_cell.open_cell = True
            self.open_around(clicked_cell)
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
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
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

    def open_all(self):
        for list_but in self.button:
            for but in list_but:
                but.open_cell = True
                if but.mine:
                    but.config(relief=tk.SUNKEN, text='*', background='red',
                               state=tk.DISABLED, disabledforeground='black')
                else:
                    if but.around_mines:
                        but.config(relief=tk.SUNKEN, text=but.around_mines,
                                   disabledforeground=but.colors[but.around_mines],
                                   state=tk.DISABLED)
                    else:
                        but.config(relief=tk.SUNKEN, text='', state=tk.DISABLED)

    def setting(self):
        win_sett = tk.Toplevel(self.win)
        win_sett.geometry(f'300x200')
        win_sett.wm_title('Настройки')
        tk.Label(win_sett, text='Мины').grid(row=0, column=1)
        tk.Label(win_sett, text='Размер поля').grid(row=1, column=1)
        mine_new = tk.Entry(win_sett)
        size_new = tk.Entry(win_sett)

        def use_new_setting():
            try:
                mine = int(mine_new.get())
                size = int(size_new.get())
                self.restart(mine, size)
                win_sett.destroy()
            except ValueError:
                win_sett.destroy()

        mine_new.grid(row=0, column=0, padx=20, pady=25)
        size_new.grid(row=1, column=0, padx=20, pady=25)
        but_ok = tk.Button(win_sett, text='Ok', width=3)
        but_ok.grid(row=2, column=2, sticky='e')
        but_ok.config(command=use_new_setting)

    def get_menu(self):
        menubar = tk.Menu(self.win)
        self.win.config(menu=menubar)

        setting_menu = tk.Menu(menubar, tearoff=0)
        setting_menu.add_command(label='game', command=self.setting)
        setting_menu.add_command(label='restart', command=self.restart)
        menubar.add_cascade(label='setting', menu=setting_menu)

    def restart(self, mines=10, size=10):
        for butts in self.button:
            for but in butts:
                but.destroy()
        self.__init__(mines, size)
        self.place_mines()
        self.count_mines()
        self.show()

    def start(self):
        self.place_mines()
        self.count_mines()
        self.show()
        self.get_menu()
        self.win.mainloop()


gp = Gamebutton()
gp.start()
