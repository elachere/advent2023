from math import inf

from pydantic import BaseModel


class MapLine(BaseModel):
    map_number: int
    src_start: int
    dst_start: int
    rangel: int


class Map(BaseModel):
    lines: list[MapLine]


class Pipeline(BaseModel):
    maps: list[Map]

    def run(self, seed: int):
        n = seed
        for _map in self.maps:
            n = match(_map, n)

        return n


def match(_map: Map, n: int):
    for line in _map.lines:
        if line.src_start <= n < line.src_start + line.rangel:
            return line.dst_start + (n - line.src_start)

    return n


def parse_input(filename: str = "../input.txt"):
    seeds: list[int] = []
    maps: list[Map] = []

    with open(filename) as f:
        line = f.readline()
        seeds = [int(x) for x in line[line.find(":") + 2 :].split()]
        f.readline()
        content = f.read().split("\n\n")

    i = 1
    for line in content:
        _map = Map(lines=[])

        for rawmap in line.split("\n")[1:]:
            dst_start, src_start, rangel = [int(x) for x in rawmap.split()]
            _map.lines.append(
                MapLine(
                    map_number=i,
                    src_start=src_start,
                    dst_start=dst_start,
                    rangel=rangel,
                )
            )
        maps.append(_map)
        i += 1

    return seeds, maps


def main():
    _min = inf
    seeds, maps = parse_input()
    pipeline = Pipeline(maps=maps)

    for seed in seeds:
        location = pipeline.run(seed)
        if location < _min:
            _min = location

    return _min


if __name__ == "__main__":
    print(SystemExit(main()))
