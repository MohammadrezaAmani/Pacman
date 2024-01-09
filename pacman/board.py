from pacman.agent import Agent
from pacman.config import Consts
from pacman.utils import convert_char


class Board:
    def __init__(self, board: str) -> None:
        self._board = []
        self.size = tuple()
        self.board = board

    @property
    def board(self) -> str:
        return self._board

    @board.setter
    def board(self, value: str) -> None:
        self._board = []
        if isinstance(value, Board):
            self._board = [agent.__class__(agent.x, agent.y) for agent in value._board]
            return
        value = value.strip().split("\n")
        for i in range(len(value)):
            value[i] = value[i].strip()
            for j in range(len(value[i])):
                agent_type = convert_char(value[i][j])
                if agent_type:
                    self._board.append(agent_type(i, j))
        self.size = (len(value), len(value[0]))

    def find(self, x: int, y: int):
        for i in range(len(self._board)):
            if self._board[i].is_in(x, y):
                return i

    def find_thing(self, thing):
        if isinstance(thing, Agent):
            return self.find(thing.x, thing.y)
        elif isinstance(thing, str):
            for i in range(len(self._board)):
                if self._board[i].name == thing:
                    return i

    def manhattan(self, thing: Agent, thing2: Agent):
        return abs((thing.x - thing2.x) % self.size[0]) + abs(
            (thing.y - thing2.y) % self.size[1]
        )

    def replace(self, thing: Agent, thing2: Agent):
        thing1_in_board = self.find_thing(thing)
        thing2_in_board = self.find_thing(thing2)
        if thing1_in_board is not None and thing2_in_board is not None:
            x, y = self._board[thing1_in_board].location
            self._board[thing1_in_board].move(
                self._board[thing2_in_board].x, self._board[thing2_in_board].y
            )
            self._board[thing2_in_board].move(x, y)
            return True
        return False

    def fake_replace(self, thing: Agent, thing2: Agent):
        newboard = Board(self)
        newboard.replace(thing, thing2)
        return newboard

    def find_nearest(self, thing: Agent, thing2: Agent):
        # TODO: Implement this method
        pass

    def move(self, thing: Agent, direction: str):
        thing_in_board = self.find_thing(thing)
        if direction == Consts.UP:
            self._board[thing_in_board].up()
        elif direction == Consts.DOWN:
            self._board[thing_in_board].down()
        elif direction == Consts.LEFT:
            self._board[thing_in_board].left()
        elif direction == Consts.RIGHT:
            self._board[thing_in_board].right()
