from collections import Counter
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class HandKind(str, Enum):
    FIVE_OF_k = "FIVE_OF_K"
    FOUR_OF_k = "FOUR_OF_K"
    FULL_HOUSE = "FULL_HOUSE"
    THREE_OF_k = "THREE_OF_K"
    TWO_PAIRS = "TWO_PAIRS"
    ONE_PAIR = "ONE_PAIR"
    HIGH_CARD = "HIGH_CARD"


class Hand(BaseModel):
    cards: str

    @property
    def kind(self) -> HandKind:
        cards_count = Counter(self.cards)
        iter_counts = iter(cards_count.most_common())
        next_max_count = next(iter_counts)[1]

        if next_max_count == 5:
            return HandKind.FIVE_OF_k
        elif next_max_count == 4:
            return HandKind.FOUR_OF_k
        elif next_max_count == 3:
            next_max_count = next(iter_counts)[1]
            if next_max_count == 2:
                return HandKind.FULL_HOUSE
            else:
                return HandKind.THREE_OF_k
        elif next_max_count == 2:
            next_max_count = next(iter_counts)[1]
            if next_max_count == 2:
                return HandKind.TWO_PAIRS
            else:
                return HandKind.ONE_PAIR

        return HandKind.HIGH_CARD


class Player(BaseModel):
    bet: int
    hand: Hand
    number: int
    rank: Optional[int] = None


class CamelPoker(BaseModel):
    DECK: dict[str, int] = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    HANDKIND_STRENGTH: dict[str, int] = {
        HandKind.FIVE_OF_k.value: 600,
        HandKind.FOUR_OF_k.value: 500,
        HandKind.FULL_HOUSE.value: 400,
        HandKind.THREE_OF_k.value: 300,
        HandKind.TWO_PAIRS.value: 200,
        HandKind.ONE_PAIR.value: 100,
        HandKind.HIGH_CARD.value: 0,
    }

    players: list[Player]

    def rank_players(self):
        players_by_rank = sorted(
            self.players,
            key=lambda player: (
                self.HANDKIND_STRENGTH[player.hand.kind.value],
                self.DECK[player.hand.cards[0]],
                self.DECK[player.hand.cards[1]],
                self.DECK[player.hand.cards[2]],
                self.DECK[player.hand.cards[3]],
                self.DECK[player.hand.cards[4]],
            ),
        )
        return players_by_rank

    def evaluate(self):
        return sum((i + 1) * player.bet for i, player in enumerate(self.rank_players()))


def parse_input(filename="../input.txt"):
    i = 1
    players: list[Player] = []

    with open(filename) as f:
        for line in f:
            cards, bet = line.split()
            players.append(Player(hand=Hand(cards=cards), bet=int(bet), number=i))
            i += 1

    return CamelPoker(players=players)


def main():
    game = parse_input()
    return game.evaluate()


if __name__ == "__main__":
    print(SystemExit(main()))
