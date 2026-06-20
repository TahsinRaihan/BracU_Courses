inp1 = open('input1b.txt', 'r')
out1 = open('output1b.txt', 'w')

x = inp1.readline().split(' ')
check = int(x[1])

new = inp1.readline().split(' ')

l = []
for i in new:
    l.append(int(i))

def find_pair_with_sum(arr, target_sum):
    left = 0
    right = len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]

        if current_sum == target_sum:
            return (left + 1, right + 1)  
        elif current_sum < target_sum:
            left += 1
        else:
            right -= 1

    return "IMPOSSIBLE"


result = find_pair_with_sum(l, check)
if type(result) == tuple:
    print('{} {}'.format(result[0], result[1]),file=out1)
else:
    print('{}'.format(result),file=out1)


out1.close()