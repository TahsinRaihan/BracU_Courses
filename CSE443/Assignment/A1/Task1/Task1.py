blosum62_str = """
   A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y
A  4  0 -2 -1 -2  0 -2 -1 -1 -1 -1 -1 -1 -1 -1  1  0  0 -3 -2
C  0  9 -3 -4 -2 -3 -3 -1 -3 -1 -1 -3 -3 -3 -3 -1 -1 -1 -2 -2
D -2 -3  6  2 -3 -1 -1 -3 -1 -4 -3  1 -1  0 -2  0 -1 -3 -4 -3
E -1 -4  2  5 -3 -2  0 -3  1 -3 -2  0 -1  2  0 -1 -1 -2 -3 -2
F -2 -2 -3 -3  6 -3 -1  0 -3  0  0 -3 -4 -3 -3 -2 -2 -1  1  3
G  0 -3 -1 -2 -3  6 -2 -4 -2 -4 -3  0 -2 -2 -2  0 -2 -3 -2 -3
H -2 -3 -1  0 -1 -2  8 -3 -1 -3 -2  1 -2  0  0 -1 -2 -3 -2  2
I -1 -1 -3 -3  0 -4 -3  4 -3  2  1 -3 -3 -3 -3 -2 -1  3 -3 -1
K -1 -3 -1  1 -3 -2 -1 -3  5 -2 -1  0 -1  1  2  0 -1 -2 -3 -2
L -1 -1 -4 -3  0 -4 -3  2 -2  4  2 -3 -3 -2 -2 -2 -1  1 -2 -1
M -1 -1 -3 -2  0 -3 -2  1 -1  2  5 -2 -2  0 -1 -1 -1  1 -1 -1
N -1 -3  1  0 -3  0  1 -3  0 -3 -2  6 -2  0  0  1  0 -3 -4 -2
P -1 -3 -1 -1 -4 -2 -2 -3 -1 -3 -2 -2  7 -1 -2 -1 -1 -2 -4 -3
Q -1 -3  0  2 -3 -2  0 -3  1 -2  0  0 -1  5  1  0 -1 -2 -2 -1
R -1 -3 -2  0 -3 -2  0 -3  2 -2 -1  0 -2  1  5 -1 -1 -3 -3 -2
S  1 -1  0 -1 -2  0 -1 -2  0 -2 -1  1 -1  0 -1  4  1 -2 -3 -2
T  0 -1 -1 -1 -2 -2 -2 -1 -1 -1 -1  0 -1 -1 -1  1  5  0 -2 -2
V  0 -1 -3 -2 -1 -3 -3  3 -2  1  1 -3 -2 -2 -3 -2  0  4 -3 -1
W -3 -2 -4 -3  1 -2 -2 -3 -3 -2 -1 -4 -4 -2 -3 -3 -2 -3 11  2
Y -2 -2 -3 -2  3 -3  2 -1 -2 -1 -1 -2 -3 -1 -2 -2 -2 -1  2  7
"""

matrix = {}
lines = blosum62_str.strip().split('\n')
headers = lines[0].split()
for line in lines[1:]:
    parts = line.split()
    row_char = parts[0]
    for idx, val in enumerate(parts[1:]):
        col_char = headers[idx]
        matrix[(row_char, col_char)] = int(val)

with open('Task1.txt', 'r') as f:
    lines = f.read().strip().split('\n')
    v = lines[0]
    w = lines[1]

gap_open = 11
gap_ext = 1

n = len(v)
m = len(w)

lower = [[-float('inf')] * (m + 1) for i in range(n + 1)]
middle = [[-float('inf')] * (m + 1) for j in range(n + 1)]
upper = [[-float('inf')] * (m + 1) for k in range(n + 1)]

middle[0][0] = 0

for i in range(1, n + 1):
    lower[i][0] = -gap_open - (i - 1) * gap_ext
    middle[i][0] = lower[i][0]

for j in range(1, m + 1):
    upper[0][j] = -gap_open - (j - 1) * gap_ext
    middle[0][j] = upper[0][j]

for i in range(1, n + 1):
    for j in range(1, m + 1):
        lower[i][j] = max(lower[i - 1][j] - gap_ext, middle[i - 1][j] - gap_open)
        upper[i][j] = max(upper[i][j - 1] - gap_ext, middle[i][j - 1] - gap_open)
        match_score = matrix.get((v[i - 1], w[j - 1]), 0)
        middle[i][j] = max(lower[i][j], middle[i - 1][j - 1] + match_score, upper[i][j])

i, j = n, m
v_aligned = []
w_aligned = []
matrix_state = 'M'

while i > 0 or j > 0:
    if i > 0 and j > 0 and matrix_state == 'M':
        if middle[i][j] == lower[i][j]:
            matrix_state = 'X'
        elif middle[i][j] == upper[i][j]:
            matrix_state = 'Y'
        else:
            v_aligned.append(v[i-1])
            w_aligned.append(w[j-1])
            i -= 1
            j -= 1
    elif i > 0 and matrix_state == 'X':
        v_aligned.append(v[i-1])
        w_aligned.append('-')
        if lower[i][j] == middle[i-1][j] - gap_open:
            matrix_state = 'M'
        i -= 1
    elif j > 0 and matrix_state == 'Y':
        v_aligned.append('-')
        w_aligned.append(w[j-1])
        if upper[i][j] == middle[i][j-1] - gap_open:
            matrix_state = 'M'
        j -= 1
    else:
        if i > 0:
            v_aligned.append(v[i-1])
            w_aligned.append('-')
            i -= 1
        else:
            v_aligned.append('-')
            w_aligned.append(w[j-1])
            j -= 1

v_aligned.reverse()
w_aligned.reverse()

with open('Task1_output.txt', 'w') as out:
    out.write(str(middle[n][m]) + '\n')
    out.write("".join(v_aligned) + '\n')
    out.write("".join(w_aligned) + '\n')

