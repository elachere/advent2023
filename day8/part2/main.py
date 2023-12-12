from pydantic import BaseModel


class Direction(BaseModel):
    left: str
    right: str


class Path(BaseModel):
    d_map: dict[str, Direction]
    directions: str
    currents: list[str] = []
    directions_idx: int = 0
    steps: int = 0

    def __iter__(self):
        return self

    def __next__(self):
        if all([curr.endswith("Z") for curr in self.currents]):
            raise StopIteration
        else:
            _dir = self.directions[self.directions_idx]

            for i, current in enumerate(self.currents):
                if _dir == "L":
                    self.currents[i] = self.d_map[current].left
                else:
                    self.currents[i] = self.d_map[current].right

                self.steps += 1

            if self.directions_idx == len(self.directions) - 1:
                self.directions_idx = 0
            else:
                self.directions_idx += 1

            return self.currents


def parse_input(filename: str = "../input.txt"):
    directions: str
    d_map: dict[str, Direction] = {}
    currents = []

    with open(filename) as f:
        directions = f.readline().strip("\n")
        f.readline()

        for line in f:
            key, direction = line.split(" = ")
            left, right = direction.split(", ")
            left = left.strip("(")
            right = right.strip(")\n")

            if key.endswith("A"):
                currents.append(key)

            d_map[key] = Direction(left=left, right=right)

    path = Path(d_map=d_map, directions=directions, currents=currents)

    return path


def main():
    path = parse_input()
    i = 0

    while True:
        try:
            _next = next(path)
            print(_next)
        except StopIteration:
            return i
        else:
            i += 1

    return i


if __name__ == "__main__":
    print(SystemExit(main()))
