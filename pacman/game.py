import math

from pacman.algorithm import minimax
from pacman.board import Board
from pacman.config import Consts


class Game:
    def __init__(self, initial_board: str) -> None:
        self.board = Board(initial_board)

    def play(self):
        depth = 3
        move = self.minimax_decision(depth)
        self.board.move(Consts.PACMAN, move)
        print("Pacman moved:", move)
        print("Current Board:")
        self.print_board()

    def minimax_decision(self, depth: int) -> str:
        legal_moves = [Consts.UP, Consts.DOWN, Consts.LEFT, Consts.RIGHT]
        best_move = ""
        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf

        for move in legal_moves:
            new_board = self.board.fake_replace(Consts.PACMAN, move)
            value = minimax(new_board, depth - 1, alpha, beta, False)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, value)

        return best_move

    def print_board(self):
        for i in range(self.board.size[0]):
            for j in range(self.board.size[1]):
                agent = next((a for a in self.board._board if a.is_in(i, j)), None)
                print(agent if agent else ".", end=" ")
            print()
