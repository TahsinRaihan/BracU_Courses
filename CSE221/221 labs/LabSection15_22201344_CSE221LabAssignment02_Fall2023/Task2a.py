#Task2_a

inp=open('input2a.txt','r')
out=open('output2a.txt','w')

a=inp.readline()
u=inp.readline().split(' ')


b=inp.readline()
v=inp.readline().split(' ')



l=[]
def merger(l1,l2):
    for i in l1:
        l.append(int(i))

    for j in l2:
        l.append(int(j))



    return(l)

x=merger(u,v)
y=x.sort()

for item in x:
    print(item,file=out,end=" ")





