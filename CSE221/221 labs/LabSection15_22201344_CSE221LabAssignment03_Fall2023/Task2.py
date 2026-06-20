inp = open('input2.txt', 'r')
out = open('output2.txt', 'w')

arr_len = int(inp.readline())
arr = list(map(int, inp.readline().split()))


def find_max(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_h = arr[:mid]
        right_h = arr[mid:]

        find_max(left_h)
        find_max(right_h)

        i = j = 0
        max_val = 0

        while i < len(left_h) and j < len(right_h):
            if left_h[i] > right_h[j]:
                if left_h[i] > max_val:
                    max_val = left_h[i] 
                i += 1
            else:
                if right_h[j] > max_val:
                    max_val = right_h[j] 
                j += 1

        while i < len(left_h):
            max_val = max(left_h[i], max_val)
            i += 1

        while j < len(right_h):
            max_val = max(right_h[j], max_val)
            j += 1
    
        return max_val

if len(arr)==1:
    out.write(str(arr[0]))

else:
    x=find_max(arr)
    out.write(str(x))

inp.close()
out.close()


