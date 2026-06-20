arr=[9,-4,-5,2,1,7,-4,5]
low=0
h=len(arr)-1
def max_sub_arry(arr,l,h):
    if l>h:
        return(float('-inf'))
    if l==h:
        return(arr[l])
    else:
        mid=(l+h)//2
        left_sum=max_sub_arry(arr,l,mid-1)
        right_sum=max_sub_arry(arr,mid+1,h)
        cross_sum=cross_sum_arr(arr,l,mid,h)
        return(max(left_sum,right_sum,cross_sum))
    
def cross_sum_arr(arr,l,mid,h):
    left_sum=float('-inf')
    sum=0
    for i in range(mid,l-1,-1):
        sum+=arr[i]
        cross_left_sum=max(sum,left_sum)
    
    right_sum=float('-inf')
    sum=0
    for j in range(mid,h+1,1):
        sum+=arr[j]
        cross_right_sum=max(sum,right_sum)

    return(cross_left_sum+cross_right_sum-arr[mid])

x=max_sub_arry(arr,low,h)
print(x)


