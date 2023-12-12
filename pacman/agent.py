from pacman.config import Consts


class Agent:
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        enemy: str = None,
        favorite: str = None,
        pts: int = None,
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.enemy = enemy
        self.favorite = favorite

    def move(self, x: int, y: int):
        self.x = x
        self.y = y

    def up(self):
        self.y -= 1

    def down(self):
        self.y += 1

    def right(self):
        self.x += 1

    def left(self):
        self.x -= 1

    def get_id(self, x, y):
        return

    def is_in(self, x: int, y: int) -> bool:
        return self.x == x and self.y == y

    @property
    def location(self) -> tuple:
        return (self.x, self.y)

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"{type(self).__name__!r}({self.x},{self.y})"


class Pacman(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(
            Consts.PACMAN,
            x,
            y,
            enemy=[Consts.GHOST1, Consts.GHOST2],
            favorite=Consts.DOT,
            pts=1,
        )


class Ghost1(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(
            Consts.GHOST1, x, y, enemy=None, favorite=[Consts.PACMAN], pts=-1
        )


class Ghost2(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(
            Consts.GHOST2, x, y, enemy=None, favorite=[Consts.PACMAN], pts=-1
        )


class Dot(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(Consts.DOT, x, y, enemy=None, favorite=None)


class Wall(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(Consts.WALL, x, y, enemy=None, favorite=None)
