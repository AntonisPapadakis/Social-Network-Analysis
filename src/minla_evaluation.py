from math import factorial
from scipy import stats
import pandas as pd
import directories as d
import os


def main():
    # CSV to party dictionary 
    fname = os.path.join(d.data_dir, "dataset.csv")
    df = pd.read_csv(fname, delimiter=';')
    party_id = dict(zip(df.id, df.Party))

    parties_order = []
    tau_scores = []
    for snapshot in range(19, 49):
        # Minla txt to mapping list
        fname = os.path.join(d.layouts_dir, f"{snapshot}.txt")
        with open(fname) as f:
            minla = [party_id[int(id.strip('\n'))] for id in f.readlines()]


        # Get list of lists 
        l = sorted(minla)
        parties = []
        for i in range(6):
            parties.append([i] * l.count(i))


        # get permutations
        def permutations(elements):
            if len(elements) <= 1:
                yield elements
                return
            for perm in permutations(elements[1:]):
                for i in range(len(elements)):
                    # nb elements[0:1] works in both string and list contexts
                    yield perm[:i] + elements[0:1] + perm[i:]

        p = list(permutations(parties))

        perm = []
        for i in p:
            a = []
            for j in i:
                for k in j:
                    a.append(k)
            perm.append(a)

        # Taub
        best_tau = -1
        for p in perm:
            tau, _ = stats.kendalltau(p, minla)
            if tau > best_tau:
                best_permutation = p
                best_tau = tau
        # print(best_permutation)
        best_permutation = list(dict.fromkeys(best_permutation))
        best_permutation.remove(0)
        # print(best_permutation)
        
        # id to party name
        party_name = {
            0: 'Ανεξάρτητοι',
            1: 'ΜΕΡΑ25',
            2: 'ΣΥΡΙΖΑ',
            3: 'ΚΙΝΑΛ',
            4: 'Νέα Δημοκρατία',
            5: 'Ελληνική Λύση'
        }

        party_order = [party_name[i] for i in best_permutation] 
        parties_order.append(party_order)
        tau_scores.append(round(best_tau, 2))
    
    df = pd.DataFrame(zip(range(19, 49), parties_order),
                              columns=['Snapshot', 'Party Order'])
    fname = os.path.join(d.tables_dir, "party_order.csv")
    df.to_csv(fname)
    
    df = pd.DataFrame(zip(range(19, 49), tau_scores),
                              columns=['Snapshot', 'Tau Score'])
    
    fname = os.path.join(d.tables_dir, "minla_eval.csv")
    df.to_csv(fname)


if __name__ == "__main__":
    main()