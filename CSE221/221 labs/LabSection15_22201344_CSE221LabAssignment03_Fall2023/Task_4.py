inp=open('input4.txt','r')
out=open('output4.txt','w')

arr_len=int(inp.readline())
arr1=list(map(int,inp.readline().split()))



arr2=[]

for i in arr1:
    arr2.append(i**2)



def max_index(arr2):
    max=arr2[1]
    max_idx=1
    for i in range(1,arr_len):
        if arr2[i]>max:
            max=arr2[i]
            max_idx=i
    return(max,max_idx)




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




max_val,max_idx=max_index(arr2)

new_arr=arr1[:max_idx+1]

res_arr=[]
for i in range(0,len(new_arr)):
    if i==max_idx:
        continue
    else:
        res_arr.append(new_arr[i])
        

output_i=mergeSort(new_arr)



result=output_i[-1]+max_val

print(result,file=out)

inp.close()
out.close()

