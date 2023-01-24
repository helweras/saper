from random import choice


class Cell:
    '''Объявлен класс Cell, который является клеткой на поле'''
    def __init__(self, mine, around_mines=0, fl_open=False):
        self.around_mines = around_mines  #Колличество мин вокруг клетки, колличество считается в методе count_mine класса GamePole
        self.mine = mine #Является ли клетка миной(True - является миной)
        self.fl_open = fl_open #Открыта или нет клетка на игровом поле(False - закрыта)


class GamePole:
    '''Объявлен класс GamePole который является игровым полем и содержит основные методы
    для работы, а так же атрибуты для обязательной передачи:N - размероность поля NхN
                                                            М - колличество мин на поле'''
    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.pole = [[Cell(False) for _ in range(N)] for _ in range(N)]
        self.init()
        self.count_mines()
        self.show()

    def init(self):
        x = 0
        while x != self.M:
            c = choice(choice(self.pole))
            if c.mine:
                continue
            else:
                c.mine = True
                x += 1

    def count_mine(self, i, j):
        if not self.pole[i][j].mine:
            for x in range(i - 1, i + 2):
                for c in range(j - 1, j + 2):
                    if x not in range(0, self.N) or c not in range(0, self.N):
                        continue
                    else:
                        if self.pole[x][c].mine:
                            self.pole[i][j].around_mines += 1

    def count_mines(self):
        for i in range(self.N):
            for j in range(self.N):
                self.count_mine(i, j)

    def show(self):

        for i in range(self.N):
            for j in range(self.N):
                if self.pole[i][j].mine:
                    print('#', end=' ')
                else:
                    print(self.pole[i][j].around_mines, end=' ')
            print()


pole_game = GamePole(10, 12)

