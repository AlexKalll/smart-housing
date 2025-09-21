import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

class HousePricePredictor:
    def init(self):
        # Simulate training a model (in real scenario, we have to use actual dataset)

        #Total rows: 1000
        #Columns: 4 (size, bedrooms, age, price)

        np.random.seed(42)
        self.data = pd.DataFrame({
            'size': np.random.uniform(1000, 5000, 1000), # 1,2,3,4  Generates 1000 random float values 
            'bedrooms': np.random.randint(1, 6, 1000),   # Generates 1000 random integer values
            'age': np.random.uniform(0, 50, 1000),
            'price': None
        })
        
        # Create synthetic price based on features
        self.data['price'] = (
            self.data['size'] * 0.2 + 
            self.data['bedrooms'] * 50000 - 
            self.data['age'] * 1000 + 
            np.random.normal(0, 50000, 1000)
        )
        
        # Prepare the model
        X = self.data[['size', 'bedrooms', 'age']]
        y = self.data['price']
        
        # Split and scale data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        
        # Train model
        self.model = LinearRegression()
        self.model.fit(X_train_scaled, y_train)
        
        # Save scaler and model
        joblib.dump(scaler, 'scaler.joblib')
        joblib.dump(self.model, 'ml_model.joblib')

# Why is this important?

# Ensures all features are on the same scale
# Prevents features with larger magnitudes from dominating the machine learning model
# Improves the performance and convergence of many machine learning algorithms
    


    def predict(self, size, bedrooms, age):
        # Load saved model and scaler
        scaler = joblib.load('scaler.joblib')
        model = joblib.load('ml_model.joblib')

        # insert our inpute to scaler then it will convert it and then insert the converted scaler format to prediction format
        
        # Prepare input
        input_data = np.array([[size, bedrooms, age]])
        input_scaled = scaler.transform(input_data)
        
        # Predict
        prediction = model.predict(input_scaled)[0]
        return round(prediction, 2)
    
HousePricePredictor().init()
