arr = [9, 8, 7, 2, 3, 4, 5, 1, 6]

def quicksort(arr, low, high):
    if low < high:
        p = partition(arr, low, high)
        quicksort(arr, low, p)
        quicksort(arr, p + 1, high)

def partition(arr, low, high):
    pivot = arr[low]
    i = low
    for j in range(low + 1, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i], arr[low] = pivot, arr[i]
    return i

low = 0
high = len(arr)
quicksort(arr, low, high)
print(arr)
