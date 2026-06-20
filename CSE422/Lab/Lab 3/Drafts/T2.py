def evaluate_sequence(sequence, target, weights):
    """Compute utility = -sum(weights[i] * abs(ord(sequence[i]) - ord(target[i])))"""
    total = 0
    length = max(len(sequence), len(target))
    for i in range(length):
        w = weights[i] if i < len(weights) else 1
        s_val = ord(sequence[i]) if i < len(sequence) else 0
        t_val = ord(target[i]) if i < len(target) else 0
        total += w * abs(s_val - t_val)
    return -total


def minimax_search(choices, prefix, target, weights, boost_factor,alpha, beta, is_maximizer):
    if not choices:
        return prefix, evaluate_sequence(prefix, target, weights)

    if is_maximizer:
        best_value, best_seq = float('-inf'), None
        for idx, nucleotide in enumerate(choices):
            remaining = choices[:idx] + choices[idx+1:]
            candidate = prefix + nucleotide

            # apply boost if we just picked 'S'
            if nucleotide == 'S':
                pick_index = len(prefix)
                boosted = weights.copy()
                for j in range(pick_index, len(boosted)):
                    boosted[j] *= boost_factor
            else:
                boosted = weights

            seq, val = minimax_search(remaining, candidate, target,boosted, boost_factor,max(alpha, best_value), beta,False)
            if val > best_value:
                best_value, best_seq = val, seq
            if best_value >= beta:
                break
        return best_seq, best_value

    else:
        worst_value, worst_seq = float('inf'), None
        for idx, nucleotide in enumerate(choices):
            remaining = choices[:idx] + choices[idx+1:]
            seq, val = minimax_search(remaining, prefix + nucleotide,target, weights, boost_factor,alpha, min(beta, worst_value),True)
            if val < worst_value:
                worst_value, worst_seq = val, seq
            if worst_value <= alpha:
                break
        return worst_seq, worst_value


# --- Process multiple cases from input_2.txt ---

lines = [line.strip() for line in open('input 2.txt') if line.strip()]
first_case = True
for i in range(0, len(lines), 3):
    if not first_case:
        print()
    first_case = False

    pool = lines[i].split(',')           # ['A','T','C','G']
    target_sequence = lines[i+1]
    sid_digits = list(map(int, lines[i+2].split()))

    # derive position weights and boost factor
    position_weights = sid_digits[-len(target_sequence):]
    boost_factor = (sid_digits[0] * 10 + sid_digits[1]) / 100.0

    # normal game utility (only score needed)
    _, normal_score = minimax_search(pool, '', target_sequence,position_weights, boost_factor,float('-inf'), float('inf'), True)

    # special game with 'S'
    special_pool = pool + ['S']
    best_sequence, special_score = minimax_search(special_pool, '', target_sequence,position_weights, boost_factor,float('-inf'), float('inf'), True)

    # output
    print('NO' if special_score <= normal_score else 'YES')
    print('With special nucleotide')
    print(f"Best gene sequence generated: {best_sequence},")
    print(f"Utility score: {special_score:.2f}")
