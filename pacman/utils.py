from pacman.agent import Agent, Dot, Ghost1, Ghost2, Pacman, Wall
from pacman.config import Consts

CONVERT_TABLE = {
    Consts.GHOST1: Ghost1,
    Consts.GHOST2: Ghost2,
    Consts.DOT: Dot,
    Consts.WALL: Wall,
    Consts.PACMAN: Pacman,
}


def convert_char(char: str) -> Agent:
    return CONVERT_TABLE[char] if char in CONVERT_TABLE else None


def turn_char(depth: int):
    return {
        2: Consts.GHOST1,
        1: Consts.GHOST2,
        0: Consts.PACMAN,
    }[depth % 3]
