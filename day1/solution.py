def first_int(line: str):
    i = 0
    while True:
        try:
            r = int(line[i])
        except ValueError:
            i += 1
        else:
            return str(r)


with open("input.txt") as f:
    lines = f.read().split()


_sum = 0
for line in lines:
    _sum += int(first_int(line) + first_int(line[::-1]))

print(_sum)
