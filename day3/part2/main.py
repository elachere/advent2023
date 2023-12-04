from pydantic import BaseModel


class Point(BaseModel):
    x: int
    y: int
    value: str
    posnumber: int  # if the point is part of a number, this is the position in this number, -1 if not part of a number

    @property
    def is_number(self) -> bool:
        return self.posnumber > 0


class Map(BaseModel):
    width: int
    height: int
    points: dict[tuple[int, int], Point]

    def __call__(self, x: int, y: int) -> Point:
        return self.points[(x, y)]

    def pprint_line(self, x: int):
        print("".join([self(x, y).value for y in range(self.width)]))

    def find_ajdacents(self, point: Point) -> list[Point]:
        adjacents = []
        for x in [-1, 0, 1]:
            if point.x + x >= 0 and point.x + x <= self.height:
                for y in [-1, 0, 1]:
                    if point.y + y >= 0 and point.y + y <= self.width:
                        if not (x == 0 and y == 0):
                            adjacents.append(self.points[(point.x + x, point.y + y)])

        return adjacents

    def parse_number(self, x: int, y: int) -> (int, int):
        """
        For any point that is part of a number, return the value of this
        number.
        """

        strn = ""
        point = self(x, y)
        current = self(x, point.y - (point.posnumber - 1))

        while current.is_number:
            strn += current.value

            if current.y >= self.width:
                break

            current = self(current.x, current.y + 1)

        return int(strn)


def parse_map(filename: str = "../input.txt") -> Map:
    _map = Map(points={}, width=0, height=0)

    with open(filename) as f:
        x = 0
        for line in f:
            y = 0
            for char in line:
                try:
                    int(char)
                except ValueError:
                    posnumber = -1
                else:
                    posnumber = posnumber + 1 or 1

                if char != "\n":
                    point = Point(x=x, y=y, value=char, posnumber=posnumber)
                    _map.points[(x, y)] = point
                    y += 1
            x += 1

    _map.width = y - 1
    _map.height = x - 1
    return _map


def main():
    x, y = 0, 0
    numbers = []
    _map = parse_map()
    gear = "*"

    while x <= _map.height:
        y = 0
        while y <= _map.width:
            next_y = -1

            if _map(x, y).value == gear:
                adj = _map.find_ajdacents(_map(x, y))
                adj_numbers = list(
                    set(
                        [
                            _map.parse_number(point.x, point.y)
                            for point in adj
                            if point.is_number
                        ]
                    )
                )
                if len(adj_numbers) == 2:
                    numbers.append(adj_numbers[0] * adj_numbers[1])

            if next_y > 0:
                y = next_y
            else:
                y += 1
        x += 1

    print(sum(numbers))


if __name__ == "__main__":
    print(SystemExit(main()))
