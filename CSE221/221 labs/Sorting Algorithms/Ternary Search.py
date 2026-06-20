arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
key = 8

def ternary_search(arr, key):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3

        if arr[mid1] == key:
            return mid1
        elif arr[mid2] == key:
            return mid2
        elif arr[mid1] > key:
            high = mid1 - 1
        elif key > arr[mid2]:
            low = mid2 + 1

    return -1

idx = ternary_search(arr, key)
print(idx)
