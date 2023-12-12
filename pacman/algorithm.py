import math
from pacman.agent import Dot
from pacman.utils import turn_char
from pacman.board import Board
from pacman.config import Consts


def evaluate(board: Board, agent: str) -> int:
    pacman_pos = board.find_thing(Consts.PACMAN)
    dot_positions = [
        board.find_thing(Consts.DOT)
        for i in range(len(board._board))
        if isinstance(board._board[i], Dot)
    ]
    ghost1_pos = board.find_thing(Consts.GHOST1)
    ghost2_pos = board.find_thing(Consts.GHOST2)

    pacman_score = 0
    ghost_score = 0

    for dot_pos in dot_positions:
        distance = board.manhattan(board._board[pacman_pos], board._board[dot_pos])
        pacman_score += 1 / (distance + 1)

    ghost_score += 1 / (
        board.manhattan(board._board[pacman_pos], board._board[ghost1_pos]) + 1
    )
    ghost_score += 1 / (
        board.manhattan(board._board[pacman_pos], board._board[ghost2_pos]) + 1
    )

    return pacman_score - ghost_score


def heuristic(board: Board, agent: str) -> int:
    agent_pos = board.find_thing(agent)
    dots = [
        board.find_thing(Consts.DOT)
        for i in range(len(board._board))
        if isinstance(board._board[i], Dot)
    ]
    min_distance = math.inf

    for dot in dots:
        distance = board.manhattan(board._board[agent_pos], board._board[dot])
        if distance < min_distance:
            min_distance
            min_distance = distance

    return min_distance


def minimax(board: Board, depth: int, maximizing_player: bool) -> int:
    if depth == 0:
        return evaluate(board, Consts.PACMAN)

    legal_moves = [Consts.UP, Consts.DOWN, Consts.LEFT, Consts.RIGHT]
    if maximizing_player:
        max_eval = -math.inf
        for move in legal_moves:
            new_board = board.fake_replace(Consts.PACMAN, turn_char(move))
            eval = minimax(new_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for move in legal_moves:
            new_board = board.fake_replace(Consts.GHOST1, turn_char(move))
            eval = minimax(new_board, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


"---------------------------ALPHA BETA PRUNING------------------------------"


def minimax_(
    board: Board, depth: int, alpha: float, beta: float, maximizing_player: bool
) -> int:
    if depth == 0:
        return evaluate(board, Consts.PACMAN)

    legal_moves = [Consts.UP, Consts.DOWN, Consts.LEFT, Consts.RIGHT]
    if maximizing_player:
        max_eval = -math.inf
        for move in legal_moves:
            new_board = board.fake_replace(Consts.PACMAN, move)
            eval = minimax_(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in legal_moves:
            new_board = board.fake_replace(Consts.GHOST1, move)
            eval = minimax_(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def minimax_decision(self, depth: int) -> str:
    legal_moves = [Consts.UP, Consts.DOWN, Consts.LEFT, Consts.RIGHT]
    best_move = ""
    best_value = -math.inf
    alpha = -math.inf
    beta = math.inf

    for move in legal_moves:
        new_board = self.board.fake_replace(Consts.PACMAN, move)
        value = minimax_(new_board, depth - 1, alpha, beta, False)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, value)

    return best_move


"---------------------------A* SEARCH------------------------------"


def a_star_search(board: Board, goal_state: str) -> list:
    frontier = [board]
    explored = set()

    while frontier:
        current_board = frontier.pop(0)
        explored.add(current_board)

        if current_board.find_thing(goal_state) is not None:
            return reconstruct_path(current_board, explored)

        for move in [Consts.UP, Consts.DOWN, Consts.LEFT, Consts.RIGHT]:
            new_board = current_board.fake_replace(Consts.PACMAN, move)

            if new_board not in explored:
                new_board.heuristic = heuristic(new_board, Consts.PACMAN)
                frontier.append(new_board)

        frontier.sort(key=lambda x: x.heuristic)

    return None


def reconstruct_path(current_board: Board, explored: set) -> list:
    path = []
    while current_board is not None:
        path.append(current_board)
        current_board = next(
            (
                explored_board
                for explored_board in explored
                if current_board.find_thing(Consts.PACMAN)
                == explored_board.find_thing(Consts.PACMAN)
            ),
            None,
        )

    path.reverse()
    return path


"---------------------------GAME CLASS------------------------------"
