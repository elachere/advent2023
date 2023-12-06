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

        for _map in self.maps[::-1]:
            n = match(_map, n)

        return n


def process_map_line(line: MapLine, n: int):
    if line.dst_start <= n < line.dst_start + line.rangel:
        return line.src_start + (n - line.dst_start)
    return None


def match(_map: Map, n: int):
    for line in _map.lines:
        r = process_map_line(line, n)

        if r is not None:
            return r

    return n


def parse_input(filename: str = "../input.txt"):
    seeds_input: list[int] = []
    maps: list[Map] = []

    with open(filename) as f:
        line = f.readline()
        seeds_input = [int(x) for x in line[line.find(":") + 2 :].split()]

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

    return seeds_input, maps


def main():
    _min = inf
    seeds_input, maps = parse_input()
    pipeline = Pipeline(maps=maps)

    location = 0
    while True:
        r = pipeline.run(location)
        for start, _range in [
            seeds_input[i : i + 2] for i in range(0, len(seeds_input), 2)
        ]:
            if start <= r < start + _range:
                return location

        location += 1

    return _min


if __name__ == "__main__":
    print(SystemExit(main()))
