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
