arr = [9, 8, 7, 2, 3, 4, 5, 1, 6]

def mergesort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_h = arr[:mid]
        right_h = arr[mid:]

        mergesort(left_h)
        mergesort(right_h)

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

print(mergesort(arr))
