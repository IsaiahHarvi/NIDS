import os
import pandas as pd

def collect_data():
    """
    Collects all pandas readable CSV files in data/CIC.
    """
    files = [f"data/CIC/{csv}" for csv in os.listdir("data/CIC") if csv.endswith('.csv')]
    for file in files:
        print(f"Checking {file}...", end="   ")

        try:
            pd.read_csv(file)
            print(f"OK")
        except Exception as e:
            print("X")
            print(f"\t{e}\n")
            files.remove(file)
    print(end="\n\n")
    return files

if __name__ == "__main__":
    collect_data()