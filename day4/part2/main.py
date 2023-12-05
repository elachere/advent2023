from functools import cached_property

from pydantic import BaseModel


class Card(BaseModel):
    number: int
    instances: int = 1
    winners: list[int]
    numbers: list[int]

    def __add__(self, x: int):
        self.instances += x
        return self

    @property
    def value(self) -> int:
        return len([x for x in self.numbers if x in self.winners])


class Game(BaseModel):
    cards: list[Card]

    @cached_property
    def size(self):
        return len(self.cards)

    def value(self) -> int:
        return sum(card.instances for card in self.cards)

    def pprint(self) -> None:
        print("\n".join(str(card) for card in self.cards))


def parse_input(filename: str = "../input.txt") -> Game:
    game = Game(cards=[])
    i = 1

    with open(filename) as f:
        for line in f:
            line = " ".join(line.split())
            winners = line[line.find(":") + 2 : line.find("|")].strip().split(" ")
            numbers = line[line.find("|") + 1 :].replace("  ", "").strip().split(" ")
            winners = [int(x) for x in winners]
            numbers = [int(x) for x in numbers]
            game.cards.append(
                Card(number=i, instances=1, winners=winners, numbers=numbers)
            )
            i += 1

    return game


def main():
    game = parse_input()

    for card in game.cards:
        value = card.value
        instances = card.instances

        if value + card.number <= game.size:
            for i in range(value):
                game.cards[card.number + i] += instances

        elif card.number < game.size:
            game.cards[card.number] += 1

    return game.value()


if __name__ == "__main__":
    print(SystemExit(main()))
