import pandas as pd
import mlflow
import mlflow.sklearn
import os
import zipfile
import urllib.request
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score



def ensure_dataset():
    if not os.path.exists("data/bank.csv"):
        print("📥 Downloading dataset...")
        url = "https://archive.ics.uci.edu/static/public/222/bank+marketing.zip"
        zip_path = "data/bank.zip"
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall("data/")
        print("✅ Dataset downloaded and extracted.")
    else:
        print("✅ Dataset already exists. Cannot be downloaded.")


def train_and_save_model():
    ensure_dataset()
    df = pd.read_csv("data/bank.csv", sep=";")
    df = df.dropna()

    X = df.drop("y", axis=1)
    y = df["y"].apply(lambda x: 1 if x == "yes" else 0)
    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    mlflow.set_experiment("Bank_Marketing_Drift_Demo")

    with mlflow.start_run():
        mlflow.log_params(model.get_params())
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")

    os.makedirs("mlruns/models", exist_ok=True)
    joblib.dump(model, "mlruns/models/random_forest.pkl")

    return accuracy
