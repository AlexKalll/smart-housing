import os
from pathlib import Path
import numpy as np
import pandas as pd
import random

root_dir = Path(__file__).parent.parent
data_dir = root_dir / "data"
csv_data = data_dir / "housing.csv"

LOCATIONS = ["Downtown", "Suburbs", "Rural"]
HOUSE_TYPES = ["Villa", "Apartment", "L-shape", "Normal"]

cols = ["size", "bedrooms", "age", "location", "house_type", "price"]


def _price_adjustments(location: str, house_type: str) -> float:
    loc_adj = {
        "Downtown": 1.20,
        "Suburbs": 1.00,
        "Rural": 0.85,
    }[location]
    type_adj = {
        "Villa": 1.15,
        "Apartment": 0.95,
        "L-shape": 1.03,
        "Normal": 1.00,
    }[house_type]
    return loc_adj * type_adj


def generate_rows(n_rows: int) -> pd.DataFrame:
    sizes = np.random.randint(1000, 5000, size=n_rows)
    bedrooms = np.random.randint(1, 6, size=n_rows)
    ages = np.random.randint(0, 51, size=n_rows)

    locs = np.random.choice(LOCATIONS, size=n_rows)
    types = np.random.choice(HOUSE_TYPES, size=n_rows)

    base_prices = sizes * 1000 + bedrooms * 500 - ages * 300
    # Categorical features
    adj = np.array([
        _price_adjustments(loc, typ) for loc, typ in zip(locs, types)
    ])
    # add variation of ±20%
    var_factor = np.random.uniform(0.8, 1.2, size=n_rows)
    prices = (base_prices * adj * var_factor).astype(float).round(2)

    df = pd.DataFrame({
        "size": sizes.astype(int),
        "bedrooms": bedrooms.astype(int),
        "age": ages.astype(int),
        "location": locs,
        "house_type": types,
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