class BoardException(Exception):
    pass


class BoardWrongShipException(BoardException):
    def __str__(self):
        return "Вы пытаетесь разместить корабдь за полем"


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


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
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size

        self.field = [["0"] * size for _ in range(size)]

        self.destroyed_ships = 0
        self.busy_cells = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " | "

        if self.hid:
            res = res.replace("■", "0")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = " ■ "
            self.busy.append(d)

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
                        self.field[cur.x][cur.y] = "  .  "
                    self.busy_cells.append(cur)


f = Board()
print(f.contour(Ship(Dot(1, 2), 4, 0)))
