
inp= open('input_1a.txt', 'r')
out = open('output_1a.txt', 'w')

def find_representative(a):
    if parents[a] == a:
        return a
    return find_representative(parents[a])


def union(a, b):
    u = find_representative(a)
    v = find_representative(b)
    if u != v:
        parents[u] = v
        circles[v] += circles[u]
    out.write(str(circles[v]) + '\n')

people, queries = map(int, inp.readline().split())
parents = [i for i in range(people)]
circles = [1 for _ in range(people)]



for _ in range(queries):
    a, b = map(int, inp.readline().split())
    union(a, b)


inp.close()
out.close()
