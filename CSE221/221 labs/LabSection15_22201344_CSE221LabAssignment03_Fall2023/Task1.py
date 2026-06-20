inp = open('input1.txt', 'r')
out = open('output1.txt', 'w')

len_arr = int(inp.readline())  

arr1 = list(map(int, inp.readline().split()))  

def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_h = arr[:mid]
        right_h = arr[mid:]

        mergeSort(left_h)
        mergeSort(right_h)

        i = j = k = 0

        while i < len(left_h) and j < len(right_h):
            if left_h[i] < right_h[j]:
                arr[k] = left_h[i]
                i += 1
            else:
                arr[k] = right_h[j]
                j += 1
            k += 1

        while i < len(left_h):
            arr[k] = left_h[i]
            i += 1
            k += 1

        while j < len(right_h):
            arr[k] = right_h[j]
            j += 1
            k += 1

    return arr

mergeSort(arr1)




out.write(" ".join(map(str, arr1)))

inp.close()
out.close()

