from random import randint


class BoardException(Exception):
    pass


class BoardWrongShipException(BoardException):
    def __str__(self):
        return "Вы пытаетесь разместить корабдь за полем"


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, cell, lives, direction):
        self.cell = cell
        self.lives = lives
        self.direction = direction

    def dots(self):
        ship_dots = []
        for i in range(self.lives):
            cur_x = self.cell.x
            cur_y = self.cell.y

            if self.direction == 0:
                cur_x += i

            elif self.direction == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots()


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в это место."


class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size

        self.field = [["O"] * size for _ in range(size)]

        self.destroyed_ships = 0
        self.busy_cells = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "   | 1  | 2  | 3  | 4  | 5  | 6  |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " | "

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def add_ship(self, ship):

        for d in ship.dots():
            if self.out(d) or d in self.busy_cells:
                raise BoardWrongShipException()
        for d in ship.dots():
            self.field[d.x][d.y] = "■"
            self.busy_cells.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots():
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy_cells:
                    if verb:
                        self.field[cur.x][cur.y] = " . "
                    self.busy_cells.append(cur)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy_cells:
            raise BoardUsedException()

        self.busy_cells.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.destroyed_ships += 1
                    self.contour(ship, verb=True)
                    print("Убит!")
                    return False
                else:
                    print("Потбил!")
                    return True

        self.field[d.x][d.y] = " . "
        print("Мимо!")
        return False

    def begin(self):
        self.busy_cells = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход врага: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Куда стреляем?: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for laa in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), laa, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def intro(self):
        print("    МОРСКОЙ БОЙ    ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Ваше поле:")
            print(self.us.board)
            print("-" * 20)
            print("Поле врага:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ваш ход!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.destroyed_ships == 7:
                print("-" * 20)
                print("Вы выиграли!")
                break

            if self.us.board.destroyed_ships == 7:
                print("-" * 20)
                print("Вы проиграли, попробуйте снова!")
                break
            num += 1

    def start(self):
        self.intro()
        self.loop()


g = Game()
g.start()
