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


def parse_input(filename: str = "../input.txt") -> list[Race]:
    races: list[Race] = []

    with open(filename, "rb") as f:
        f.seek(5)
        times = [int(x) for x in " ".join(f.readline().decode("utf-8").split()).split()]
        f.seek(9, 1)
        distances_to_beat = [
            int(x) for x in " ".join(f.readline().decode("utf-8").split()).split()
        ]

    for max_time, distance_to_beat in zip(times, distances_to_beat):
        races.append(Race(max_time=max_time, distance_to_beat=distance_to_beat))

    return races


def main():
    races = parse_input()
    return prod(race.nb_better for race in races)


if __name__ == "__main__":
    print(SystemExit(main()))
