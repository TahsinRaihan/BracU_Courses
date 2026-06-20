# minimax_task2.py

def build_position_weights(sid_digits, n):
    # last n digits of SID
    return sid_digits[-n:]

def compute_utility(gene, target, weights):
    """Utility = –∑ wi·|ASCII(gene[i])–ASCII(target[i])|;
       out-of-bounds chars count as 0, default wi=1."""
    total = 0
    N = max(len(gene), len(target))
    for i in range(N):
        w = weights[i] if i < len(weights) else 1
        g = ord(gene[i]) if i < len(gene) else 0
        t = ord(target[i]) if i < len(target) else 0
        total += w * abs(g - t)
    return -total

def minimax_ab(pool, built, target, weights, α, β, maximizer,
               booster_factor=None, s_picked_at=None):
    """
    If booster_factor is set, then as soon as 'S' is picked at position k:
    all subsequent weights w[i>=k] are multiplied by booster_factor.
    """
    if not pool:
        return built, compute_utility(built, target, weights)

    if maximizer:
        best_val, best_seq = -float('inf'), None
        for i, nuc in enumerate(pool):
            rem      = pool[:i] + pool[i+1:]
            new_seq  = built + nuc
            # if we just picked 'S', note its position and adjust weights
            if nuc == 'S' and s_picked_at is None and booster_factor is not None:
                k = len(built)
                # apply booster to all weights from k onward
                boosted = weights.copy()
                for j in range(k, len(boosted)):
                    boosted[j] *= booster_factor
            else:
                boosted = weights

            seq, val = minimax_ab(
                rem,
                new_seq,
                target,
                boosted,
                α, β,
                False,
                booster_factor,
                s_picked_at if s_picked_at is not None else (len(built) if nuc=='S' else None)
            )
            if val > best_val:
                best_val, best_seq = val, seq
            α = max(α, best_val)
            if β <= α:
                break
        return best_seq, best_val

    else:
        best_val, best_seq = float('inf'), None
        for i, nuc in enumerate(pool):
            rem     = pool[:i] + pool[i+1:]
            new_seq = built + nuc
            seq, val = minimax_ab(
                rem,
                new_seq,
                target,
                weights,
                α, β,
                True,
                booster_factor,
                s_picked_at
            )
            if val < best_val:
                best_val, best_seq = val, seq
            β = min(β, best_val)
            if β <= α:
                break
        return best_seq, best_val

# ———— Input & Execution ————

with open('input 2.txt') as f:
    lines = [L.strip() for L in f if L.strip()]

first = True
for i in range(0, len(lines), 3):
    if not first:
        print()    # blank line between cases
    first = False

    pool   = lines[i].split(',')       # e.g. ["A","T","C","G"]
    target = lines[i+1]                # e.g. "ATGC"
    sid    = list(map(int, lines[i+2].split()))

    # 1) Normal game
    weights      = build_position_weights(sid, len(target))
    normal_gene, normal_util = minimax_ab(
        pool, "", target, weights,
        -float('inf'), float('inf'), True
    )

    # 2) Special game (add 'S' + booster)
    special_pool = pool + ['S']
    booster      = (sid[0]*10 + sid[1]) / 100.0
    special_gene, special_util = minimax_ab(
        special_pool, "", target, weights.copy(),
        -float('inf'), float('inf'), True,
        booster_factor=booster
    )

    # Decide if special helps
    print("YES" if special_util > normal_util else "NO")
    print("With special nucleotide")
    print(f"Best gene sequence generated: {special_gene}")
    print(f"Utility score: {special_util:.2f}")
