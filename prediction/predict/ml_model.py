from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split  
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

root_dir = Path(__file__).resolve().parents[2]
data_path = root_dir / "data" / "housing.csv"
checkpoints_dir = root_dir / "checkpoints"
scaler_dir = checkpoints_dir / "scaler.joblib"
model_dir = checkpoints_dir / "model_latest.joblib"

class HousePricePredictor:
    LOCATIONS = ["Downtown", "Suburbs", "Rural"]
    HOUSE_TYPES = ["Villa", "Apartment", "L-shape", "Normal"]

    def __init__(self):
        self.data_path = data_path
        self.checkpoints_dir = checkpoints_dir
        self.scaler_path = scaler_dir
        self.model_path = model_dir
        self.numeric_cols = ["size", "bedrooms", "age"]
        self.expected_cat_cols = ( [f"location_{c}" for c in self.LOCATIONS] + [f"house_type_{c}" for c in self.HOUSE_TYPES])

    def load_dataset(self) -> pd.DataFrame:
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset not found at {self.data_path}. Generate it with scripts/data_generator.py.")
        
        df = pd.read_csv(self.data_path)
        return df

    def prepare_features(self, df: pd.DataFrame):
        # Separate numeric + categorical
        X_num = df[self.numeric_cols]
        # One-hot encode categorical features
        X_cat = pd.get_dummies(
            df[["location", "house_type"]],
            columns=["location", "house_type"], dtype=int)
        y = df["price"].astype(float)
        return X_num, X_cat, y

    def train_and_save_model(self) -> None:
        """Train model and save to checkpoints/"""
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

        df = self.load_dataset()
        X_num, X_cat, y = self.prepare_features(df)

        train_idx, val_idx = train_test_split(df.index, test_size=0.2, random_state=42, shuffle=True)

        X_num_tr, X_num_va = X_num.loc[train_idx], X_num.loc[val_idx]
        X_cat_tr, X_cat_va = X_cat.loc[train_idx], X_cat.loc[val_idx]
        y_tr, y_va = y.loc[train_idx], y.loc[val_idx]

        # Scale numeric features 
        scaler = StandardScaler()
        X_num_tr_scaled = scaler.fit_transform(X_num_tr)
        X_num_va_scaled = scaler.transform(X_num_va)

        # build final training matrices
        X_tr = np.hstack([X_num_tr_scaled, X_cat_tr.values])
        X_va = np.hstack([X_num_va_scaled, X_cat_va.values])

        # Train model
        model = LinearRegression()
        model.fit(X_tr, y_tr)

        # Save artifacts
        joblib.dump({"scaler": scaler, "expected_cat_cols": self.expected_cat_cols, "numeric_cols": self.numeric_cols }, self.scaler_path )
        joblib.dump(model, self.model_path)

    def retrain_and_save_model(self) -> None:
        self.train_and_save_model()

    def predict_price( self, size: float, bedrooms: int, age: int, location: str, house_type: str,) -> float:
        """Load model and predict price for new input"""
        if not (self.scaler_path.exists() and self.model_path.exists()):
            self.train_and_save_model()

        artifacts = joblib.load(self.scaler_path)
        scaler: StandardScaler = artifacts["scaler"]
        expected_cat_cols = artifacts["expected_cat_cols"]
        numeric_cols = artifacts.get("numeric_cols", self.numeric_cols)
        model: LinearRegression = joblib.load(self.model_path)

        # numeric input
        X_num_row = pd.DataFrame([[float(size), int(bedrooms), int(age)]], columns=numeric_cols)

        # categorical input
        cat_dict = {col: 0 for col in expected_cat_cols}
        cat_dict[f"location_{location}"] = 1
        cat_dict[f"house_type_{house_type}"] = 1
        X_cat_row = pd.DataFrame([cat_dict], columns=expected_cat_cols).astype(int)

        X_num_scaled = scaler.transform(X_num_row)
        X_all = np.hstack([X_num_scaled, X_cat_row.values])

        pred = float(model.predict(X_all)[0])
        return round(pred, 2)

def train_and_save_model() -> None:
    return HousePricePredictor().train_and_save_model()

def retrain_and_save_model() -> None:
    return HousePricePredictor().retrain_and_save_model()

def predict_price(size: float, bedrooms: int, age: int, location: str, house_type: str) -> float:
    return HousePricePredictor().predict_price(size, bedrooms, age, location, house_type)
