# Task_4

inp4=open('input4.txt','r')
out4=open('output4.txt','w')

num_entries = int(inp4.readline())

train_info = []

for i in range(num_entries):
    entry_parts = inp4.readline().split(" ")
    train_info.append((entry_parts[0], entry_parts[4], entry_parts[6][:-1]))


for i in range(num_entries):
     max_index = i
     for j in range(i, num_entries):
        if train_info[max_index][0] > train_info[j][0]:
            max_index = j
        elif train_info[max_index][0] == train_info[j][0]:
            if train_info[max_index][2] < train_info[j][2]:
                 max_index = j

     train_info[i], train_info[max_index] = train_info[max_index], train_info[i]

for i in range(num_entries):
        print('{} will depart for {} at {}'.format(train_info[i][0],train_info[i][1],train_info[i][2]),file=out4)

out4.close()