import math

from pacman.algorithm import minimax
from pacman.board import Board
from pacman.config import Consts


class Game:
    def __init__(self, initial_board: str) -> None:
        self.board = Board(initial_board)

    def play(self):
        depth = 3
        while not self.board.is_finished():
            self.board.display()
            if self.board.turn_char(depth) == Consts.PACMAN:
                self.board = minimax(self.board, depth, True)
            else:
                self.board = minimax(self.board, depth, False)
            depth += 1
