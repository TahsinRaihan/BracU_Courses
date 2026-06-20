#Task_2

input_file = open('input2.txt', 'r')
output_file = open('output2.txt', 'w')


def bubble_sort(arr):
    sorted_flag = True
    for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1],     arr[i]
                    sorted_flag = False
        
    return arr


lines = input_file.readlines()

for i in range(1, len(lines), 2):
    values = lines[i].split(' ')
    numbers = []

    for value in values:
        numbers.append(int(value))
        sorted_numbers = bubble_sort(numbers)

    for number in sorted_numbers:
        output_file.write(f'{number} ')
        print(numbers,end=' ')

input_file.close()
output_file.close()