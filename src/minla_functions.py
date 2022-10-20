import random
import math
import numpy as np


def simulated_annealing(adj, layout, init_temp=1000,
                        cool_ratio=0.9, stop_temp=1, mit=500, seed=0):
    len_layout = len(layout)
    cost_final = LA(adj, layout)
    layout_new = layout.copy()
    temp = init_temp
    random.seed(seed)
    # np.random.seed(1)

    while temp > stop_temp:
        for i in range(mit):
            x = random.randint(0, len_layout - 1)
            y = random.randint(0, len_layout - 1)

            layout_new[x], layout_new[y] = layout_new[y], layout_new[x]
            cost_new = LA(adj, layout_new)
            delta_cost = (cost_new - cost_final) / temp

            if delta_cost <= 0:
                cost_final = cost_new
                continue

            prob = math.exp(-delta_cost)
            # if np.random.random_sample() <= min(1.0, prob):
            if random.random() <= min(1.0, prob):
                cost_final = cost_new
            else:
                layout_new[x], layout_new[y] = layout_new[y], layout_new[x]

        temp *= cool_ratio
    return layout_new, cost_final


def LA(G, s):
    n = len(s)
    ncosts = int((n ** 2 - n) / 2)
    costs = np.zeros(ncosts)
    cnt = 0
    for i in range(n - 1):
        src = s[i]
        for j in range(i + 1, n):
            trgt = s[j]
            costs[cnt] = G[src, trgt] * (j - i)
            cnt += 1
    la = np.sum(costs)
    return la


def full_search(G, sequence):
    n = len(G)
    minCost = LA(G, sequence)
    z = cnt = 0
    while z < 1:
        z = z + 1
        print(minCost)
        sequence, newCost = SelectBestNeighbor(G, sequence)
        if newCost < minCost:
            z = 0
            cnt += 1
            minCost = newCost
    return sequence, minCost, cnt


def SelectBestNeighbor(G, sequence):
    n = len(G)
    minCost = LA(G, sequence)
    ii = jj = 0
    for i in range(n - 1):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        for j in range(i + 1, n):
            sequence[i], sequence[j] = sequence[j], sequence[i]
            newCost = LA(G, sequence)
            if newCost < minCost:
                minCost, ii, jj = newCost, i, j
            sequence[i], sequence[j] = sequence[j], sequence[i]
    sequence[ii], sequence[jj] = sequence[jj], sequence[ii]
    
    return sequence, minCost