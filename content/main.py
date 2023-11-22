import math


class Consts:
    GHOST1 = "G1"
    GHOST2 = "G2"
    DOT = "."
    WALL = "#"
    PACMAN = "P"
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


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


CONVERT_TABLE = {
    Consts.GHOST1: Ghost1,
    Consts.GHOST2: Ghost2,
    Consts.DOT: Dot,
    Consts.WALL: Wall,
    Consts.PACMAN: Pacman,
}


def _convert_char(char: str) -> Agent:
    return CONVERT_TABLE[char] if char in CONVERT_TABLE else None


def _turn_char(depth: int):
    return {
        2: Consts.GHOST1,
        1: Consts.GHOST2,
        0: Consts.PACMAN,
    }[depth % 3]


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
                agent_type = _convert_char(value[i][j])
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
            new_board = board.fake_replace(Consts.PACMAN, _turn_char(move))
            eval = minimax(new_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for move in legal_moves:
            new_board = board.fake_replace(Consts.GHOST1, _turn_char(move))
            eval = minimax(new_board, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


"---------------------------ALPHA BETA PRUNING------------------------------"


def minimax(
    board: Board, depth: int, alpha: float, beta: float, maximizing_player: bool
) -> int:
    if depth == 0:
        return evaluate(board, Consts.PACMAN)

    legal_moves = [Consts.UP, Consts.DOWN, Consts.LEFT, Consts.RIGHT]
    if maximizing_player:
        max_eval = -math.inf
        for move in legal_moves:
            new_board = board.fake_replace(Consts.PACMAN, move)
            eval = minimax(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in legal_moves:
            new_board = board.fake_replace(Consts.GHOST1, move)
            eval = minimax(new_board, depth - 1, alpha, beta, True)
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
        value = minimax(new_board, depth - 1, alpha, beta, False)
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


def main():
    initial_board = """
    #######
    #P#...#
    #.#...#
    #.#G#.#
    #...#.#
    #...#.#
    #######
    """
    game = Game(initial_board)
    game.play()

if __name__ == "__main__":
    main()
