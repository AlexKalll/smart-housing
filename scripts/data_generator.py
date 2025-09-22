import os
from pathlib import Path
import numpy as np
import pandas as pd
import random

root_dir = Path(__file__).parent.parent
data_dir = root_dir / "data"
csv_data = data_dir / "housing.csv"

cols = ["size", "bedrooms", "age", "price"]

def generate_rows(n_rows: int) -> pd.DataFrame:
    sizes = np.random.randint(1000, 5000, size=n_rows)
    bedrooms = np.random.randint(1, 6, size=n_rows)
    ages = np.random.randint(0, 51, size=n_rows)

    base_prices = sizes * 300 + bedrooms * 10000 - ages * 500
    # add variation of ±20%
    var_factor = np.random.uniform(0.8, 1.2, size=n_rows)
    prices = (base_prices * var_factor).astype(float).round(2)

    df = pd.DataFrame({
        "size": sizes.astype(int),
        "bedrooms": bedrooms.astype(int),
        "age": ages.astype(int),
        "price": prices,
    }, columns=cols)
    return df

def main():
    data_dir.mkdir(parents=True, exist_ok=True)
    n_rows = random.randint(100, 200)
    df_new = generate_rows(n_rows)

    if csv_data.exists() and csv_data.stat().st_size > 0:
        old_df = pd.read_csv(csv_data)        
        if old_df.empty:
            df_new.to_csv(csv_data, mode="w", header=True, index=False)
            print(f"Recreated {csv_data} with {n_rows} rows (was empty).")
        else:
            df_new.to_csv(csv_data, mode="a", header=False, index=False)
            print(f"Appended {n_rows} rows to {csv_data}.")
    else:
        df_new.to_csv(csv_data, mode="w", header=True, index=False)
        print(f"Dataset created with {n_rows} rows.")

if __name__ == "__main__":
    main()