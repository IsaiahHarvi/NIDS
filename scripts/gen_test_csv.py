import os
from collections import Counter

import pandas as pd


def main():
    dfs = [pd.read_csv(f"data/CIC/{f}", delimiter="\t") for f in os.listdir("data/CIC")]
    df = pd.concat(dfs, ignore_index=True)

    class_counts = Counter(df["label"])
    print("Class counts:")
    for label, count in class_counts.items():
        print(f"  {label}: {count}")

    distribution = {
        "benign": 200000,
        "ddos": 100000,
    }
    capped = []
    for label, _ in distribution.items():
        class_data = df[df["label"] == label]

        sampled_data = class_data.sample(distribution[label])
        capped.append(sampled_data)

    capped_df = pd.concat(capped, ignore_index=True)
    capped_df.to_csv("data/CIC/test_data.csv", index=False, sep="\t")

    print("\nCapped counts:")
    for label, count in Counter(capped_df["label"]).items():
        print(f"  {label}: {count}")

    print("\nSaved to data/CIC/test_data.csv")


if __name__ == "__main__":
    main()
