#%%

import pandas as pd
import argparse

def parse_csv(path):
    df = pd.read_csv(path)
    df['Weight'] = df['Weight'].fillna(1)
    df.dropna(axis='rows', how='any', inplace=True)
    return df['Predicate'], df['Weight']

# %%

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to parse CSV files that consist of Predicate \
        and Weight column and return them as separate Pandas Series")
    parser.add_argument("path", type=str, help="Path to file with predicates and respective weights")

    args = parser.parse_args()
    predicates, weights = parse_csv(args.path)
    print(predicates, weights)
