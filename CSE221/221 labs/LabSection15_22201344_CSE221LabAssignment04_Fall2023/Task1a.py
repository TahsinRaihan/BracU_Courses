inp = open('input1a _1.txt', 'r')
out = open('output1a_1.txt', 'w')



v_e = list(map(int, inp.readline().split()))

ver = v_e[0]
edge = v_e[1]

matrix = []
for i in range(ver+1):
    edges = []
    for j in range(ver+1):
        edges.append(0)
    matrix.append(edges)


for i in range(0,edge):
    u, v, w = map(int, inp.readline().split())
    matrix[u][v] = w


for j in range(ver+1):
    print(matrix[j],file=out)


inp.close()
out.close()