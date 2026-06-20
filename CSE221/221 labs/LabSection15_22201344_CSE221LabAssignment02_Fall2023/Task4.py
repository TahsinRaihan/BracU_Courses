#Task_4

input_file = open("input4.txt", "r")
output_file = open("output4.txt", "w")

line = list(map(int, input_file.readline().split(" ")))
num_tasks = line[0]  
num_people = line[1]  

tasks = []   #Makinsg a list of all tasks
for item in range(num_tasks):
    line = list(map(int, input_file.readline().split(" ")))
    tasks.append(line)


def mergesort(arr):
    if len(arr) == 1:
        return arr
    else:
        mid = len(arr) // 2
        a = mergesort(arr[:mid])
        b = mergesort(arr[mid:])
        return merge(a, b)

def merge(a, b):
    i = 0
    j = 0
    new_arr = []
    while i < len(a) and j < len(b):
        if a[i][1] <= b[j][1]:
            new_arr.append(a[i])
            i += 1
        else:
            new_arr.append(b[j])
            j += 1
    if i == len(a):
        for item in range(j, len(b)):
            new_arr.append(b[item])
    else:
        for item in range(i, len(a)):
            new_arr.append(a[item])
    return new_arr


sorted_tasks = mergesort(tasks) # Sorting tasks by their end times


next_available_time = [0] * num_people
count = 0

for i in range(num_tasks):
    person_idx = -1

    for j in range(num_people):
        if next_available_time[j] <= sorted_tasks[i][0] or  next_available_time[j] < next_available_time[person_idx]:
            person_idx = j

    if person_idx != -1:
        count += 1
        next_available_time[person_idx] = sorted_tasks[i][1]

output_file.write(f"{count}")

input_file.close()
output_file.close()
