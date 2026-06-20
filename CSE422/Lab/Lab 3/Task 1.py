def build_position_weights(sid_digits, target_length): #Last 4 difit of sid-22201344
    return sid_digits[-target_length:]

def compute_utility(gene_seq, target_seq, weights):
    score = 0
    N = max(len(gene_seq), len(target_seq))
    for i in range(N):
        weight = weights[i] if i < len(weights) else 1
        gene_chacracter = ord(gene_seq[i]) if i < len(gene_seq) else 0
        target_character = ord(target_seq[i]) if i < len(target_seq) else 0
        score += weight * abs(gene_chacracter - target_character)
    return -score

def minimax_ab(pool, gene, target, weights, alpha, beta, maximizing):
    if not pool:
        return gene, compute_utility(gene, target, weights)

    if maximizing: #Agent 1
        best_val, best_seq = -float('inf'), None
        for i, ch in enumerate(pool):
            next_pool = pool[:i] + pool[i+1:]
            seq, val = minimax_ab(next_pool, gene + ch, target, weights, alpha, beta, False)
            if val > best_val:
                best_val, best_seq = val, seq
            alpha = max(alpha, best_val)
            if beta <= alpha: #prune
                break
        return best_seq, best_val

    else: #Agent 2
        best_val, best_seq = float('inf'), None
        for i, ch in enumerate(pool):
            next_pool = pool[:i] + pool[i+1:]
            seq, val = minimax_ab(next_pool, gene + ch, target, weights, alpha, beta, True)
            if val < best_val:
                best_val, best_seq = val, seq
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_seq, best_val

with open('input 1.txt', 'r') as file:
    input_lines = [line.strip() for line in file if line.strip()]

first_case = True
for i in range(0, len(input_lines), 3):
    if not first_case:
        print()
    first_case = False

    pool = input_lines[i].split(',')                       
    target = input_lines[i+1]                              
    sid = list(map(int, input_lines[i+2].split()))        

    weights = build_position_weights(sid, len(target))
    best_gene, best_utility = minimax_ab(pool, "", target, weights, -float('inf'), float('inf'), True)

    print("Best gene sequence generated:", best_gene)
    print("Utility score:", best_utility)
