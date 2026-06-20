inp = open('input_3a.txt', 'r')
out = open('output_3a.txt', 'w')

freddy = int(inp.readline().strip())

arr = [0] * (freddy + 1)

def jump_count(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 3
    
    if arr[n] == 0:
        arr[n] = jump_count(n - 1) + jump_count(n - 2)
    return arr[n]

out.write(str(jump_count(freddy)))

inp.close()
out.close()
