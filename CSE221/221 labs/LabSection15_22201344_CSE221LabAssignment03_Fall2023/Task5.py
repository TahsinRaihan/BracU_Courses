inp=open('input5.txt','r')
out=open('output5.txt','w')

arr_len=int(inp.readline())
arr1=inp.readline().split(' ')



def partition(arr,low,high):
    pivot= arr[low]
    i = low
    for j in range(i+1,high):
        if int(arr[j])<int(pivot):
            i +=1
            arr[i],arr[j] = arr[j],arr[i]
    arr[i] , arr[low] = pivot , arr[i]
    return i



def quick_sort(arr,low,high):
    if low<high:
        p = partition(arr,low,high)
        quick_sort(arr,low,p)
        quick_sort(arr,p+1,high)




sortt = quick_sort(arr1, 0, arr_len)


for i in range (arr_len):
    out.write(f"{arr1[i]} ")


inp.close()
out.close()
