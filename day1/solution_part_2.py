import re

import ipdb

numbers = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def first_int(line: str, reg):
    try:
        res = reg.search(line).group()
    except AttributeError:
        return None

    if not res.isnumeric():
        return numbers[res]

    return res


with open("input.txt") as f:
    lines = f.read().split()

# for x in range(5):
#     print(first_int(lines[x]))

reg = re.compile(f'{"|".join(numbers.values())}|{"|".join(numbers.keys())}')

_sum = 0
x = 0
for line in lines:
    first = first_int(line, reg)
    ll = len(line)
    second = None
    i = 1
    while second is None:
        second = first_int(line[ll - i : ll], reg)
        i += 1

    _sum += int(f"{first}{second}")

    # print(f"{first}{second}")
    # if x == 4:
    #     ipdb.set_trace()
    # if x == 10:
    #     break
    # x += 1


print(_sum)

# reg = f'{"|".join(numbers.values())}|{"|".join(numbers.keys())}'
# print(reg)
