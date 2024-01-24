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
        Moves: list = None,
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.enemy = enemy
        self.favorite = favorite
        self.moves = Moves if Moves else [self.up, self.down, self.right, self.left]

    def move(self, x: int, y: int):
        self.x = x
        self.y = y

    def move_dir(self, dir: str):
        {
            Consts.UP: self.up,
            Consts.DOWN: self.down,
            Consts.RIGHT: self.right,
            Consts.LEFT: self.left,
        }[
            {
                0: Consts.UP,
                1: Consts.DOWN,
                2: Consts.RIGHT,
                3: Consts.LEFT,
            }[dir] if isinstance(dir, int) else dir
        ]()

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
        return f"{type(self).__name__}({self.x},{self.y})"


class Dot(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(Consts.DOT, x, y, enemy=None, favorite=None)


class Wall(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(Consts.WALL, x, y, enemy=None, favorite=None)


class Pacman(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(
            Consts.PACMAN,
            x,
            y,
            enemy=[],
            favorite=Dot,
            pts=1,
        )


class Ghost(Agent):
    def __init__(self, name: str, x: int, y: int) -> None:
        super().__init__(name, x, y, enemy=None, favorite=[Pacman], pts=-1)
