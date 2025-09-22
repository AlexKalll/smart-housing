- This folder is like a database for house prices predictor model owned by a company that wants to predict the house prices based on size, bedrooms and age of the house.

- The data is generated using `scripts/data_generator.py` and the data is stored in `data/housing.csv`
    - It has `Size`, `Bedrooms`, `Age` and `Price` as columns
    - The `Price` column is generated based on the `Size`, `Bedrooms` and `Age` columns and it is the target variable.

- The model is trained using `prediction/predict/ml_model.py`

Note: For best practice, the `data/housing.csv` file has not been committed to the remote repository as it acts like a database.