import random
from pacman.board import Board
from pacman.config import Consts


class Game:
    def __init__(self, initial_board: str) -> None:
        self.board = Board(initial_board)

    def play(self, depth: int = 1):
        depth = depth * (len(Consts.GHOSTS) + 1)
        while not self.board.is_finished():
            # self.board.clear_screen()
            print(self.board.pacman)
            self.board.display()
            print(self.board._board)
            turn = self.board.turn_char(depth)
            if turn == Consts.PACMAN:
                self.board.pacman.move_dir(self.board.minimax(depth, self.board.pacman))
            else:
                self.board.ghosts[turn - 1].move_dir(
                    random.choice(self.board.ghosts[turn - 1].moves)
                )
