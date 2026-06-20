inp=open('input.txt','r')
out=open('output.txt','w')

ver,edge=map(int,inp.readline().split())

matrix=[]

for i in range(ver+1):
    v=[]
    for j in range(ver+1):
        v.append(0)
    matrix.append(v) 


for i in range(0,edge):
    p,q,w=map(int,inp.readline().split())
    matrix[p][q]=w

for j in matrix:
    print(j,file=out)