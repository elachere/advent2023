from pydantic import BaseModel


class Direction(BaseModel):
    left: str
    right: str


class Path(BaseModel):
    d_map: dict[str, Direction]
    directions: str
    target: str = "ZZZ"
    start: str = "AAA"
    current: str = "AAA"
    directions_idx: int = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current == self.target:
            raise StopIteration
        else:
            if self.directions[self.directions_idx] == "L":
                self.current = self.d_map[self.current].left
            else:
                self.current = self.d_map[self.current].right

            if self.directions_idx == len(self.directions) - 1:
                self.directions_idx = 0
            else:
                self.directions_idx += 1

            return self.current


def parse_input(filename: str = "../input.txt"):
    directions: str
    d_map: dict[str, Direction] = {}

    with open(filename) as f:
        directions = f.readline().strip("\n")
        f.readline()

        for line in f:
            key, direction = line.split(" = ")
            left, right = direction.split(", ")
            left = left.strip("(")
            right = right.strip(")\n")

            d_map[key] = Direction(left=left, right=right)

    path = Path(d_map=d_map, directions=directions)

    return path


def main():
    i = 0
    path = parse_input()

    while True:
        try:
            print(next(path))
        except StopIteration:
            return i
        else:
            i += 1

    return path


if __name__ == "__main__":
    print(SystemExit(main()))
