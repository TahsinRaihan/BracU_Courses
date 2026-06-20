#Task_3


inp3=open('input3.txt','r')
out3=open('output3.txt','w')

num=int(inp3.readline())
given_id=inp3.readline()
given_marks=inp3.readline()

id=[]
marks=[]

given_id=given_id.split(" ")
given_marks=given_marks.split(' ')

for i in given_id:
    id.append(int(i))
for j in given_marks:
    marks.append(int(j))

for i in range(0,num):
    max=i
    for j in range(i,num):
        if marks[j]==marks[max]:
            if id[j]<id[max]:
                max=j
        elif marks[j]>marks[max]:
            max=j
    marks[i],marks[max]=marks[max],marks[i]
    id[i],id[max]=id[max],id[i]

for i in range(0,num,1):
    output="ID: {} Marks: {}".format(id[i],marks[i])
    print(output,file=out3)