"""
Pairing Problem
===
    Consider N indexed balls from 1 to N are in an urn. The balls are taken
    successively from the urn (without reposition), randomly. We say that
    a *pairing* has ocurred if the ball with number k (1 <= k <= N) was selected
    in the k-th withdrawal.

    In this problem, consider the random variable X = number of pairings obtained
    from the N.
"""
from random import shuffle

# Creates an absolute frequency table, by repeting the experiment n times
def create_freq(n, N):
    order = [x for x in range(1, N + 1)]
    p_dict = {i: 0 for i in range(N + 1)}
    parity_hist = []
    for _ in range(n):
        urn = [x for x in range(1, N + 1)]
        shuffle(urn) # Random order
        # Get num of pairings
        num_p = len(list(filter(lambda e: e[0] == e[1], zip(order, urn))))
        p_dict[num_p] += 1
        parity_hist.append(num_p)
    mean = sum((xi*fi)/n for xi, fi in p_dict.items())
    print(f"Nº pairings (i)  |   Nº repetitions with i pairings")
    for i in p_dict.keys():
        print(f"    {str(i).zfill(2)}           |            {p_dict[i]}")


    print(f"Mean pairings = {mean}\n")
    print(f"Full pairings list = {parity_hist}")



def main():
    n = 100 # Number of repetitions
    N = 5
    create_freq(n, N)

if __name__ == '__main__':
    main()
