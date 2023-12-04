import re
from typing import Any

from pydantic import BaseModel

REDMAX = 12
GREENMAX = 13
BLUEMAX = 14


class CubeSet(BaseModel):
    red: int
    blue: int
    green: int


class Game(BaseModel):
    number: int
    cubesets: list[CubeSet]

    def is_valid(self) -> bool:
        for cubeset in self.cubesets:
            if (
                cubeset.red > REDMAX
                or cubeset.green > GREENMAX
                or cubeset.blue > BLUEMAX
            ):
                return False

        return True

    def power(self) -> int:
        reds, blues, greens = [], [], []
        for cubeset in self.cubesets:
            reds.append(cubeset.red)
            blues.append(cubeset.blue)
            greens.append(cubeset.green)

        return max(reds) * max(blues) * max(greens)


def parse_line(line: str, game_number: int, regexes: dict):
    rawsets = line.split(";")
    game = Game(number=game_number, cubesets=[])

    for rawset in rawsets:
        try:
            n_blue = int(regexes["blue"].search(rawset).group(1))
        except AttributeError:
            n_blue = 0

        try:
            n_red = int(regexes["red"].search(rawset).group(1))
        except AttributeError:
            n_red = 0

        try:
            n_green = int(regexes["green"].search(rawset).group(1))
        except AttributeError:
            n_green = 0

        game.cubesets.append(CubeSet(red=n_red, blue=n_blue, green=n_green))

    return game


def main(filename: str = "../input.txt"):
    i: int = 1
    ret: int = 0
    redreg = re.compile("(\d+) red")
    bluereg = re.compile("(\d+) blue")
    greenreg = re.compile("(\d+) green")

    with open(filename) as f:
        for line in f:
            game = parse_line(
                line.split(":")[1],
                i,
                {"blue": bluereg, "red": redreg, "green": greenreg},
            )

            ret += game.power()

            i += 1

    return ret


if __name__ == "__main__":
    print(SystemExit(main()))
