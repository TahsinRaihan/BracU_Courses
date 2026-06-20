#Task_1a

inp=open('input1a.txt','r')
out=open('output1a.txt','w')

x=inp.readline().split(' ')
num=x[0]
check=int(x[1])

new=inp.readline().split(' ')
l=[]
for i in new:
  l.append(int(i))


idx=[]

def check_sum(check):
  flag=True
  for i in range(0,len(l)):
    first=l[i]
    for j in range(1,len(l),1):
      if l[i]==l[j]:
        continue
      sum=l[i]+l[j]
      if sum==check:
        idx.append(i+1)
        idx.append(j+1)
        flag=False
        return(flag)

  return(flag)


x=check_sum(check)
if x==True:
  print('{}'.format('Impossible'),file=out)

else:
  print('{} {}'.format(idx[0],idx[1]),file=out)





