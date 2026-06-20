import math

inp = open('input_4a.txt', 'r')
out = open('output_4a.txt', 'w')

type_, target = map(int, inp.readline().strip().split())

coins = list(map(int, inp.readline().strip().split()))

def min_coin_change(type_, target, coins):
    if target == 0:
        return 0
    if target < 0:
        return math.inf
    if type_ <= 0 and target >= 1:
        return math.inf
    return min(min_coin_change(type_ - 1, target, coins), 1 + min_coin_change(type_, target - coins[type_ - 1], coins))

result = min_coin_change(type_, target, coins)

if result == math.inf:
    out.write("-1")
else:
    out.write(str(result))

inp.close()
out.close()
