inp=open('input.txt','r')
out=open('output.txt','w')

ver=list(map(int,inp.readline().split()))
print(ver)

print(ver,edge)
matrix=[]
for i in range(0,ver+1):
    matrix.append([])

l=[]
for j in range(0,edge):
    u, v, w = map(int, inp.readline().split())
    l.append(v)
    l.append(w)
    matrix[u].append(tuple(l))
    l=[]


print(matrix)

