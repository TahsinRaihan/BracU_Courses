# minimax_multi_case.py

def build_position_weights(sid_digits, target_length):
    """Last N digits of SID are the weights for positions 0…N−1."""
    return sid_digits[-target_length:]

def compute_utility(gene_sequence, target_sequence, position_weights):
    """Utility = –∑ wi·|ASCII(gene[i])–ASCII(target[i])|."""
    total = 0
    N = max(len(gene_sequence), len(target_sequence))
    for i in range(N):
        w = position_weights[i] if i < len(position_weights) else 1
        g = ord(gene_sequence[i]) if i < len(gene_sequence) else 0
        t = ord(target_sequence[i]) if i < len(target_sequence) else 0
        total += w * abs(g - t)
    return -total

def minimax_ab(pool, current_seq, target_sequence, position_weights, alpha, beta, is_maximizer):
    # Terminal: pool empty → evaluate
    if not pool:
        return current_seq, compute_utility(current_seq, target_sequence, position_weights)

    if is_maximizer:
        best_val, best_seq = -float('inf'), None
        for i, nuc in enumerate(pool):
            rest = pool[:i] + pool[i+1:]
            seq, val = minimax_ab(rest, current_seq + nuc, target_sequence,
                                  position_weights, alpha, beta, False)
            if val > best_val:
                best_val, best_seq = val, seq
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_seq, best_val

    else:
        best_val, best_seq = float('inf'), None
        for i, nuc in enumerate(pool):
            rest = pool[:i] + pool[i+1:]
            seq, val = minimax_ab(rest, current_seq + nuc, target_sequence,
                                  position_weights, alpha, beta, True)
            if val < best_val:
                best_val, best_seq = val, seq
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_seq, best_val

# —————— Top-level script ——————

# Read all non-empty lines
with open('input 1.txt', 'r') as file:
    input_lines = [line.strip() for line in file if line.strip()]

first_case = True
# Process each 3-line group as one test case
while input_lines:
    if not first_case:
        print()            # blank line between cases
    first_case = False

    pool_line      = input_lines.pop(0)
    target_sequence = input_lines.pop(0)
    sid_line       = input_lines.pop(0)

    nucleotides_pool = pool_line.split(',')           # e.g. ["A","T","C","G"]
    sid_digits       = list(map(int, sid_line.split()))  # e.g. [2,2,2,0,1,3,4,4]

    position_weights = build_position_weights(sid_digits, len(target_sequence))

    best_seq, best_score = minimax_ab(
        nucleotides_pool,
        "",                         # start with empty sequence
        target_sequence,
        position_weights,
        -float('inf'),              # α
        float('inf'),               # β
        True                        # maximizer starts
    )

    print("Best gene sequence generated:", best_seq)
    print("Utility score:", best_score)
