from pydantic import BaseModel


class Card(BaseModel):
    winners: list[int]
    numbers: list[int]

    @property
    def value(self) -> int:
        power = len([x for x in self.numbers if x in self.winners]) - 1
        if power >= 0:
            return 2**power

        return 0


class Game(BaseModel):
    cards: list[Card]

    def value(self) -> int:
        return sum(card.value for card in self.cards)


def parse_input(filename: str = "../input.txt") -> Game:
    game = Game(cards=[])

    with open(filename) as f:
        for line in f:
            line = " ".join(line.split())
            winners = line[line.find(":") + 2 : line.find("|")].strip().split(" ")
            numbers = line[line.find("|") + 1 :].replace("  ", "").strip().split(" ")
            winners = [int(x) for x in winners]
            numbers = [int(x) for x in numbers]
            game.cards.append(Card(winners=winners, numbers=numbers))

    return game


def main():
    game = parse_input()
    return game.value()


if __name__ == "__main__":
    print(SystemExit(main()))
