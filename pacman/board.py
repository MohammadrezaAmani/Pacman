from typing import List
from pacman.agent import Agent, Dot, Ghost, Pacman
from pacman.config import Consts
from pacman.utils import convert_char


class Board:
    def __init__(self, board: str) -> None:
        """
        Initialize the Board object.

        Args:
            board (str): The string representation of the board.

        Returns:
            None
        """
        self._board = []
        self.pacman: Pacman
        self.ghosts: List[Ghost] = []
        self.size = tuple()
        self.board = board
        

    @property
    def board(self) -> str:
        """
        Get the current state of the board.

        Returns:
            str: The current state of the board.
        """
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
                    if agent_type == Ghost:
                        g = Ghost(value[i][j], i, j)
                        self._board.append(g)
                        self.ghosts.append(g)
                        Consts.GHOSTS.append(value[i][j])
                    elif agent_type == Pacman:
                        self.pacman = Pacman(i, j)
                        self._board.append(self.pacman)
                    else:
                        self._board.append(agent_type(i, j))
        self.size = (len(value), len(value[0]))
        

    def __str__(self) -> str:
        """
        Return the string representation of the board.

        Returns:
            str: The string representation of the board.
        """
        board = ""
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                agent = next((a for a in self._board if a.is_in(i, j)), None)
                board += agent.name if agent else "."
            board += "\n"
        return board

    def is_finished(self) -> bool:
        """
        Check if the game is finished.

        Returns:
            bool: True if the game is finished, False otherwise.
        """
        if not any(isinstance(a, Dot) for a in self._board):
            return True

        # if ghost and pacman are in the same position

    def __repr__(self) -> str:
        return self.__str__()
    
    def display(self):
        print(self.__str__())
    
    def turn_char(self, depth: int, Ghosts: list = None) -> int:
        if Ghosts is None:
            Ghosts = self.ghosts
        return {
            0: Consts.PACMAN,
            **{i: Consts.GHOSTS[i - 1] for i in range(1, len(Ghosts) + 1)},
        }[depth % (len(Ghosts) + 1)]

