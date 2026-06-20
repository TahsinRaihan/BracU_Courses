input_file = open("input3.txt","r")
output_file = open("output3.txt","w")


num = int(input_file.readline())


time = []
for item in range(num):
    line = list(map(int,input_file.readline().split(" ")))
    time.append(line)


for i in range(num):  #Sorting time by the end time
    for j in range(num-i-1):
        if time[j][1]>time[j+1][1]:
            time[j],time[j+1]=time[j+1],time[j]

            print(time)



count=1
idx=0
task = [time[0]]
for i in range(1,num):   
    if time[idx][1]<=time[i][0]:  #If start time is bigger then he can to the task
        count+=1
        idx=i
        task.append(time[i])

output_file.write(f"{count}\n")
for item in task:
    output_file.write(f"{item[0]} {item[1]}\n")

