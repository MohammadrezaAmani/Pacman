from pacman.agent import Agent, Dot, Ghost, Pacman, Wall
from pacman.config import Consts

CONVERT_TABLE = {
    Consts.DOT: Dot,
    Consts.WALL: Wall,
    Consts.PACMAN: Pacman,
}

_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def convert_char(char: str) -> Agent:
    return (
        CONVERT_TABLE[char]
        if char in CONVERT_TABLE
        else Ghost
        if char.lower() in _ALPHABET
        else None
    )


def turn_char(depth: int, Ghosts: list) -> int:
    return {
        0: Consts.PACMAN,
        **{i: Consts.GHOSTS[i - 1] for i in range(1, len(Ghosts) + 1)},
    }[depth % (len(Ghosts) + 1)]
