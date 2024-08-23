import os
import pandas as pd

def collect_data(verbose: bool = False):
    """
    Collects all pandas readable CSV files in data/CIC.
    """
    files = [f"data/CIC/{csv}" for csv in os.listdir("data/CIC") if csv.endswith('.csv')]
    for file in files:
        if verbose: print(f"Checking {file}...", end="   ")

        try:
            pd.read_csv(file)
            if verbose: print(f"OK")
        except Exception as e:
            if verbose:
                print("X")
                print(f"\t{e}\n")
            files.remove(file)
    if verbose: print(end="\n\n")
    return files

if __name__ == "__main__":
    collect_data(verbose=True)