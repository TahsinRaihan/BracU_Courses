arr=[1,2,3,4,5,6,7,8]

key=7

def binary_search(arr,key):
    low=0
    high= len(arr)-1
    while low<=high:
        mid=(low+high)//2

        if arr[mid]==key:
            return(mid)
        
        elif arr[mid]>key:
            high=mid-1
        else:
            low=mid+1

    return(-1)

idx=binary_search(arr,key)
print(idx)