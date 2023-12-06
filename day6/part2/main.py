from math import prod

from pydantic import BaseModel


class Race(BaseModel):
    max_time: int
    distance_to_beat: int

    def calculate_distance(self, _time: int) -> int:
        return (self.max_time - _time) * _time

    def possible_distances(self) -> list[int]:
        return [self.calculate_distance(i) for i in range(1, self.max_time)]

    @property
    def nb_better(self) -> int:
        return len([x for x in self.possible_distances() if x > self.distance_to_beat])


def parse_input(filename: str = "../input.txt") -> Race:
    with open(filename, "rb") as f:
        f.seek(5)
        max_time = int("".join(f.readline().decode("utf-8").split()))
        f.seek(9, 1)
        distance_to_beat = int("".join(f.readline().decode("utf-8").split()))

    return Race(max_time=max_time, distance_to_beat=distance_to_beat)


def main():
    race = parse_input()
    return race.nb_better


if __name__ == "__main__":
    print(SystemExit(main()))
