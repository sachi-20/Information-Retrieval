import sys
import pandas as pd
import itertools


def apriori_gen(itemsets, k):
    # generate candidate itemsets by joining pairs from existing itemsets
    candidates = set([i.union(j) for i in itemsets for j in itemsets if len(i.union(j)) == k and len(i.intersection(j)) == k - 2])
    # filter candidates to keep only those whose subsets are all frequent
    candidates = {
        candidate for candidate in candidates
        if all(frozenset(subset) in itemsets for subset in itertools.combinations(candidate, k-1))
    }

    return candidates


def remove_redundant_rules(rules):
    cleaned_rules = []
    seen_combinations = set()  # track combinations already included
    
    for antecedent, consequent, support, confidence in rules:
        # merge antecedent and consequent to form a complete set (ignoring order)
        combined_set = frozenset(antecedent).union(frozenset(consequent))
        
        # add rule if this combination hasn't been seen yet
        if combined_set not in seen_combinations:
            cleaned_rules.append((antecedent, consequent, support, confidence))
            seen_combinations.add(combined_set)
    
    return cleaned_rules


def apriori(df, min_sup, min_conf):
    # count each item occurrences in the df
    item_count = pd.concat([df[col] for col in df.columns]).value_counts()
    support = item_count / len(df)
    # store 1-itemset with enough support
    freq_itemsets = {1: {frozenset([item]): support[item] for item in support[support >= min_sup].index}}
    k = 1
    while freq_itemsets[k]:
        k += 1
        # generate all candidate itemsets for k+1
        candidates = apriori_gen(freq_itemsets[k-1], k)
        freq_itemsets[k] = {}
        for candidate in candidates:
            # initialize boolean mask set to True for all rows 
            mask = pd.Series(True, index=df.index)
            # update mask to keep only rows which contain item in candidate set
            for condition in candidate:
                mask &= df.apply(lambda row: condition in row.values, axis=1)
            # count rows that contain candidate set 
            item_count = mask.sum()
            item_support = item_count / len(df)
            # store candidate set with enough support
            if item_support >= min_sup:
                freq_itemsets[k][candidate] = item_support

    if not freq_itemsets[k]:
        del freq_itemsets[k]

    rules = []
    for k, itemsets in freq_itemsets.items():
        # 1-itemset cannot make up a rule by itself
        if k == 1: continue
        for itemset in itemsets:
            # generate only association rules with exactly one item on the right 
            for antecendent in itertools.combinations(itemset, k-1):
                antecendent = frozenset(antecendent)
                # make sure right side item does not appear on the left
                consequent = itemset.difference(antecendent)
                # retrieve support calculated beforehand
                conf = freq_itemsets[k][itemset] / freq_itemsets[k-1][antecendent]
                if conf >= min_conf:
                    rules.append((antecendent, consequent, freq_itemsets[k][itemset], conf))

    rules = remove_redundant_rules(rules)
    # format frequent itemsets 
    freq_itemsets_final = [(itemset, freq_itemsets[k][itemset]) for k, itemsets in freq_itemsets.items() for itemset in itemsets]
    # sort frequent itemsets based on support
    freq_itemsets_final.sort(key=lambda x: -x[1])
    top_5_percent = int(len(freq_itemsets_final) * 0.05)
    freq_itemsets_final = freq_itemsets_final[top_5_percent:]
    # sort association rules based on confidence 
    rules.sort(key=lambda x: -x[3])
    top_5_percent_rules = int(len(rules) * 0.05)
    rules = rules[top_5_percent_rules:]

    return freq_itemsets_final, rules


def print_results(frequent_itemsets, rules, output_file, min_sup, min_conf):
    with open(output_file, 'w') as f:
        f.write(f"==Frequent itemsets (min_sup={min_sup})\n")
        for itemset, support in frequent_itemsets:
            f.write(f"{list(itemset)}, {support*100:.4f}%\n")
        f.write(f"==High-confidence association rules (min_conf={min_conf})\n")
        for antecedent, consequent, support, confidence in rules:
            f.write(f"{list(antecedent)} => {list(consequent)} (Conf: {confidence*100:.2f}%, Supp: {support*100:.4f}%)\n")
    

def main():
    if len(sys.argv) != 4:
        print("Use: python3 main.py <filename> <min_support> <min_confidence>")
        return
    
    filename = sys.argv[1]
    min_sup = float(sys.argv[2])
    min_conf = float(sys.argv[3])

    df = pd.read_csv(filename)

    freq_itemsets, rules = apriori(df, min_sup, min_conf)
    print_results(freq_itemsets, rules, "example-run.txt", min_sup, min_conf)


if __name__ == "__main__":
    main()