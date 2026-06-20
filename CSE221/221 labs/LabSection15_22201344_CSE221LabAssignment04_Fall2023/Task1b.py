inp = open('input1b_1.txt', 'r')
out = open('output1b_1.txt', 'w')

v_e = list(map(int, inp.readline().split()))

ver = v_e[0]
edge = v_e[1]



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



concat=' '
for j in range(len(matrix)):
    if len(matrix[j])==0:
        print("{} : {}".format(j,'  '),file=out)
    else:
        for k in matrix[j]:
            concat= concat + ' ' + str(k)
        print("{} : {}".format(j,concat),file=out)
        concat=' '
        

inp.close()
out.close()
