#Task_2b

inp1=open('input2b.txt','r')
out1=open('output2b.txt','w')

size1 = int(inp1.readline())-1
arr1 = list(map(int,inp1.readline().split()))
size2 = int(inp1.readline())-1
arr2 = list(map(int,inp1.readline().split()))

i = 0
j = 0
arr = []

while i<=size1 and j<=size2:
    if arr1[i]<=arr2[j]:
        arr.append(arr1[i])
        i+=1
    elif arr1[i]>arr2[j]:
        arr.append(arr2[j])
        j+=1

if i>size1:
    merged_arr = arr+arr2[j:]
if j>size2:
    merged_arr = arr+arr1[i:]

for item in merged_arr:
    out1.write(f"{item} ")
