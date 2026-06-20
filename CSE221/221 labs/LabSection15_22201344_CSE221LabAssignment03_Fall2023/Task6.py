inp = open('input6.txt', 'r')
out = open('output6.txt', 'w')

arr_len = int((inp.readline()).split(" ")[0])
arr = inp.readline().split(" ")
queries_len = int((inp.readline()).split(" ")[0])

def partition(arr, low, high):
    pivot = arr[low]
    i = low
    for j in range(i + 1, high):
        if int(arr[j]) < int(pivot):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i], arr[low] = pivot, arr[i]
    return i

def k_small(arr, low, high, k):
    if low < high:
        p = partition(arr, low, high)
        if p == k:
            return p
        elif k < p:
            return k_small(arr, low, p, k)
        else:
            return k_small(arr, p + 1, high, k)

for i in range(queries_len):
    query_num = int(inp.readline())
    sorted_index = k_small(arr, 0, arr_len, query_num - 1)
    out.write(f"{arr[sorted_index]}\n")

inp.close()
out.close()
