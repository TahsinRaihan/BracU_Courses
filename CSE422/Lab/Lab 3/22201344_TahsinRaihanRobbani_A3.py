##### Task-1 #####

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


##### Task-2 #####


def compute_utility(gene_seq, target_seq, weights):
    score = 0
    N = max(len(gene_seq), len(target_seq))
    for i in range(N):
        weight = weights[i] if i < len(weights) else 1
        gene_chacracter = ord(gene_seq[i]) if i < len(gene_seq) else 0
        target_character = ord(target_seq[i]) if i < len(target_seq) else 0
        score += weight * abs(gene_chacracter - target_character)
    return -score


def minimax_search(choices, prefix, target, weights, boost_factor,alpha, beta, is_maximizer, has_used_boost=False):
    if not choices: #means if pool is empty
        return prefix, compute_utility(prefix, target, weights)

    if is_maximizer: # Agent 1
        best_value, best_seq = float('-inf'), None
        for idx, nucleotide in enumerate(choices):
            remaining = choices[:idx] + choices[idx+1:]
            candidate = prefix + nucleotide

            if nucleotide == 'S' and not has_used_boost: #  boost if S Is picked and not done already
                pick_index = len(prefix)
                boosted = weights.copy()
                for j in range(pick_index, len(boosted)):
                    boosted[j] *= boost_factor
                next_weights = boosted
                next_used_boost = True
            else:
                next_weights = weights
                next_used_boost = has_used_boost

            seq, val = minimax_search(remaining, candidate, target,next_weights, boost_factor,max(alpha, best_value), beta,False, next_used_boost)
            if val > best_value:
                best_value, best_seq = val, seq
            if best_value >= beta:
                break
        return best_seq, best_value

    else: # Agent 2
        worst_value, worst_seq = float('inf'), None
        for idx, nucleotide in enumerate(choices):
            remaining = choices[:idx] + choices[idx+1:]
            seq, val = minimax_search(remaining, prefix + nucleotide,target, weights, boost_factor,alpha, min(beta, worst_value),True, has_used_boost)
            if val < worst_value:
                worst_value, worst_seq = val, seq
            if worst_value <= alpha:
                break
        return worst_seq, worst_value

lines = [line.strip() for line in open('input 2 .txt') if line.strip()]
first_case = True
for i in range(0, len(lines), 3):
    if not first_case:
        print()
    first_case = False

    pool = lines[i].split(',')  
    target_sequence = lines[i+1]
    sid_digits = list(map(int, lines[i+2].split()))

    position_weights = sid_digits[-len(target_sequence):]  #  position weights and boost factor
    boost_factor = (sid_digits[0] * 10 + sid_digits[1]) / 100.0

    x, normal_score = minimax_search(pool, '', target_sequence,position_weights, boost_factor,float('-inf'), float('inf'), True, False) #without s 

    special_pool = pool + ['S']
    best_sequence, special_score = minimax_search(special_pool, '', target_sequence,position_weights, boost_factor,float('-inf'), float('inf'), True, False)     # special with S

    print('NO' if special_score <= normal_score else 'YES')
    print('With special nucleotide')
    print(f"Best gene sequence generated: {best_sequence},")
    print(f"Utility score: {special_score:.2f}")
