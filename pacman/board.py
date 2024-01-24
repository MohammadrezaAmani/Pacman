import math
import os
from typing import List

from pacman.agent import Agent, Dot, Ghost, Pacman
from pacman.config import Consts
from pacman.utils import convert_char


class Board:
    def __init__(self, board: str = None) -> None:
        """
        Initialize the Board object.

        Args:
            board (str): The string representation of the board.

        Returns:
            None
        """
        self.pacman: Pacman = Pacman(0, 0)
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
            self.pacman = Pacman(value.pacman.x, value.pacman.y)
            self.ghosts = [
                Ghost(ghost.name, ghost.x, ghost.y) for ghost in value.ghosts
            ]
            self._board = [
                agent.__class__(agent.x, agent.y)
                for agent in value._board
                if not isinstance(agent, Pacman) and not isinstance(agent, Ghost)
            ]
            self.size = value.size
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
                        self.pacman.enemy.append(value[i][j])
                    elif agent_type == Pacman:
                        pacman = Pacman(i, j)
                        pacman.enemy = self.pacman.enemy.copy()
                        self.pacman = pacman
                        self._board.append(self.pacman)
                    else:
                        self._board.append(agent_type(i, j))
        self.size = (len(value), len(value[0]))

    def __setitem__(self, key: tuple, value: Agent) -> None:
        """
        Set the value of the board at the given position.

        Args:
            key (tuple): The position of the agent.
            value (Agent): The agent to be placed at the given position.

        Returns:
            None
        """
        self._board.append(value)
        value.x, value.y = key

    def __getitem__(self, key: tuple) -> Agent:
        """
        Get the agent at the given position.

        Args:
            key (tuple): The position of the agent.

        Returns:
            Agent: The agent at the given position.
        """
        return next((a for a in self._board if a.is_in(*key)), None)

    def __delitem__(self, key: tuple) -> None:
        """
        Delete the agent at the given position.

        Args:
            key (tuple): The position of the agent.

        Returns:
            None
        """
        self._board.remove(self[key])

    def __contains__(self, key: tuple) -> bool:
        """
        Check if the given position is occupied by an agent.

        Args:
            key (tuple): The position to be checked.

        Returns:
            bool: True if the position is occupied, False otherwise.
        """
        return any(a.is_in(*key) for a in self._board)

    def __len__(self) -> int:
        """
        Get the number of agents on the board.

        Returns:
            int: The number of agents on the board.
        """
        return len(self._board)

    def count(self, agent_type: type) -> int:
        """
        Count the number of agents of the given type on the board.

        Args:
            agent_type (type): The type of the agent.

        Returns:
            int: The number of agents of the given type on the board.
        """
        return sum(isinstance(a, agent_type) for a in self._board)

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

    def pacman_wins(self) -> bool:
        """
        Check if Pacman wins.

        Returns:
            bool: True if Pacman wins, False otherwise.
        """
        return self.count(Dot) == 0

    def pacman_loses(self) -> bool:
        """
        Check if Pacman loses.

        Returns:
            bool: True if Pacman loses, False otherwise.
        """
        return any(ghost.is_in(self.pacman.x, self.pacman.y) for ghost in self.ghosts)

    def is_finished(self) -> bool:
        """
        Check if the game is finished.

        Returns:
            bool: True if the game is finished, False otherwise.
        """

        return self.pacman_wins() or self.pacman_loses()

    def __repr__(self) -> str:
        return self.__str__()

    def display(self):
        print(self.__str__())

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def turn_char(self, depth: int, Ghosts: list = None) -> int:
        if Ghosts is None:
            Ghosts = self.ghosts
        return {
            0: Consts.PACMAN,
            **{i: Consts.GHOSTS[i - 1] for i in range(1, len(Ghosts) + 1)},
        }[depth % (len(Ghosts) + 1)]

    def deepcopy(self) -> "Board":
        return Board(self)

    def manhatan(self, agent1: Agent, agent2: Agent) -> int:
        return abs(agent1.x - agent2.x) + abs(agent1.y - agent2.y)

    def find_nearest(self, agent: Agent, agent_type: type) -> Agent:
        nearest = None
        for a in self._board:
            if isinstance(a, agent_type):
                if nearest is None or self.manhatan(agent, a) < self.manhatan(
                    agent, nearest
                ):
                    nearest = a
        return nearest

    def get(self, agent: Agent) -> Agent:
        for i in self._board:
            if i.is_in(agent.x, agent.y):
                return i

    def evaluate(self, agent: Agent) -> str:
        favorite = self.find_nearest(agent, agent.favorite)
        enemies = []
        if isinstance(agent.enemy, list):
            enemies = [self.find_nearest(agent, enemy) for enemy in agent.enemy]

        enemy_score = sum([self.manhatan(agent, enemy) for enemy in enemies]) * 50
        favorite_score = self.manhatan(agent, favorite)

        return -1 * (favorite_score + enemy_score)

    def best_move(self, agent: Agent, depth: int = 1, maximizing: bool = True):
        best_score = -math.inf
        best_move = None

        for move in [Consts.LEFT, Consts.RIGHT, Consts.DOWN, Consts.UP]:
            board = self.deepcopy()
            agent_copy = board.get(agent)
            agent_copy.move_dir(move)
            score = board.evaluate(agent_copy)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(
        self, depth: int, agent: Agent, maximizing: bool = True, ghost_pointer: int = 0
    ):
        if depth == 0:
            return self.evaluate(self.pacman)

        if self.pacman_wins():
            return math.inf

        if self.pacman_loses():
            return -math.inf
        if maximizing:
            best_score = -math.inf
            for move in [Consts.LEFT, Consts.RIGHT, Consts.DOWN, Consts.UP]:
                board = self.deepcopy()
                agent_copy = board.get(agent)
                print(board)
                agent_copy.move_dir(move)
                score = board.minimax(depth - 1, agent_copy, False)
                best_score = max(score, best_score)
            return best_score

        else:
            best_score = math.inf
            for move in [Consts.LEFT, Consts.RIGHT, Consts.DOWN, Consts.UP]:
                board = self.deepcopy()
                agent_copy = board.get(agent)
                agent_copy.move_dir(move)
                while ghost_pointer < len(board.ghosts):
                    best_score = min(score, best_score)
            return best_score

    def minimax_move(self, agent: Agent, depth: int = 1, maximizing: bool = True):
        best_score = -math.inf
        best_move = None

        for move in [Consts.LEFT, Consts.RIGHT, Consts.DOWN, Consts.UP]:
            board = self.deepcopy()
            agent_copy = board.get(agent)
            agent_copy.move_dir(move)
            score = board.minimax(depth - 1, agent_copy, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
