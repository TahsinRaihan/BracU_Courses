# minimax_multi_case_simple.py

def compute_weights(sid_digits, n):
    return sid_digits[-n:]

def compute_utility(gene, target, weights):
    total = 0
    N = max(len(gene), len(target))
    for i in range(N):
        w = weights[i] if i < len(weights) else 1
        g = ord(gene[i]) if i < len(gene) else 0
        t = ord(target[i]) if i < len(target) else 0
        total += w * abs(g - t)
    return -total

def minimax_ab(pool, built, target, weights, α, β, maximizer):
    if not pool:
        return built, compute_utility(built, target, weights)
    if maximizer:
        best_val, best_seq = -1e18, None
        for i, x in enumerate(pool):
            seq, val = minimax_ab(pool[:i]+pool[i+1:], built+x,
                                  target, weights, α, β, False)
            if val > best_val:
                best_val, best_seq = val, seq
            α = max(α, best_val)
            if β <= α: break
        return best_seq, best_val
    else:
        best_val, best_seq =  1e18, None
        for i, x in enumerate(pool):
            seq, val = minimax_ab(pool[:i]+pool[i+1:], built+x,
                                  target, weights, α, β, True)
            if val < best_val:
                best_val, best_seq = val, seq
            β = min(β, best_val)
            if β <= α: break
        return best_seq, best_val

# —— simplified input & loop ——

lines = [L.strip() for L in open('input 1.txt') if L.strip()]
for i in range(0, len(lines), 3):
    if i: print()  # blank line between cases
    pool    = lines[i].split(',')
    target  = lines[i+1]
    sid     = list(map(int, lines[i+2].split()))
    weights = compute_weights(sid, len(target))

    best_seq, best_score = minimax_ab(
        pool, "", target, weights, -1e18, 1e18, True
    )

    print("Best gene sequence generated:", best_seq)
    print("Utility score:", best_score)
