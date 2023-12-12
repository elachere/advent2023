from pydantic import BaseModel


class Predica(BaseModel):
    history: list[int]

    def eval_nexts(self) -> list[list[int]]:
        current = [1]
        prev = self.history
        _lsts = [prev]

        while not all([x == 0 for x in current]):
            current = [prev[i + 1] - prev[i] for i in range(len(prev) - 1)]
            _lsts.append(current)
            prev = current

        for i in range(len(_lsts) - 1, 0, -1):
            _lsts[i - 1].insert(0, _lsts[i - 1][0] - _lsts[i][0])

        return _lsts


class Report(BaseModel):
    predicas: list[Predica]

    def sum_nexts(self) -> int:
        r = 0
        for predica in self.predicas:
            r += predica.eval_nexts()[0][0]

        return r


def parse_input(filename: str = "../input.txt"):
    report: Report = Report(predicas=[])

    with open(filename) as f:
        for line in f:
            report.predicas.append(Predica(history=[int(x) for x in line.split()]))

    return report


def main():
    report = parse_input()

    return report.sum_nexts()


if __name__ == "__main__":
    print(SystemExit(main()))
