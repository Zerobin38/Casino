# roulette_core.py
import random, math
from collections import Counter

# Numbers: 0-36 (European roulette). 0 is green.
RED = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}

def is_red(n):
    return n in RED

def stats_from_history(history):
    # history: list of ints, newest first (or chronological)
    cnt = Counter(history)
    total = sum(cnt.values())
    most_common = cnt.most_common(10)
    reds = sum(1 for x in history if is_red(x))
    evens = sum(1 for x in history if x!=0 and x%2==0)
    return {"total_spins": total, "most_common": most_common, "red_share": reds/total if total else None, "even_share": evens/total if total else None}

def append_history_from_list(history, extracted_list, max_len=1000):
    # extracted_list: [n1, n2, ...] where n1 is the most recent
    # we keep newest first
    new = extracted_list + history
    return new[:max_len]

# --- Strategies simulations (simplified) ---
def simulate_strategy(strategy_name, history, n_rounds=100, bank=100.0, base_bet=1.0):
    bank_history = [bank]
    bet = base_bet
    seq = []
    for i in range(n_rounds):
        # simulate spin randomly uniform (European wheel: 0-36)
        spin = random.randint(0,36)
        win = False
        if strategy_name.startswith("Martingale"):
            # Martingale on red
            bet = bet
            if is_red(spin):
                bank += bet
                bank -= 0  # already won
                bet = base_bet
            else:
                bank -= bet
                bet = min(bank, bet*2)
        elif strategy_name.startswith("Fibonacci"):
            # simplified Fibonacci on red
            if not seq: seq = [base_bet, base_bet]
            bet = seq[-1]
            if is_red(spin):
                bank += bet
                # step back
                if len(seq)>2: seq = seq[:-2]
                else: seq = [base_bet]
            else:
                bank -= bet
                seq.append(seq[-1] + seq[-2] if len(seq)>=2 else base_bet)
        else:
            # Flat bet on red
            if is_red(spin):
                bank += base_bet
            else:
                bank -= base_bet
        bank_history.append(bank)
        if bank <= 0: break
    return {"final_bank": bank, "bank_history": bank_history, "rounds_played": len(bank_history)-1}

# Utility for testing
if __name__ == "__main__":
    hist = [random.randint(0,36) for _ in range(200)]
    print(stats_from_history(hist))
    print(simulate_strategy("Martingale (sur couleur)", hist, n_rounds=50))
