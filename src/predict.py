import joblib
import json
import pandas as pd


MODEL_PATH = r"..\models\customer_churn_model.pkl"
FEATURES_PATH = r"..\models\model_features.json"


# Load model once
model = joblib.load(MODEL_PATH)

with open(FEATURES_PATH, "r") as f:
    model_features = json.load(f)


def assign_risk(probability):
    if probability >= 0.50:
        return "High"
    elif probability >= 0.30:
        return "Medium"
    else:
        return "Low"


def recommend_action(customer, risk_level):
    actions = []

    if risk_level == "High":
        actions.append("Priority retention outreach")

    if customer["Contract"] == "Month-to-month":
        actions.append("Review longer-term contract incentive")

    if customer["TechSupport"] == "No":
        actions.append("Review Tech Support offer")

    if customer["OnlineSecurity"] == "No":
        actions.append("Review Online Security offer")

    if customer["PaymentMethod"] == "Electronic check":
        actions.append("Review automatic payment incentive")

    if not actions:
        actions.append("Standard customer engagement")

    return " | ".join(actions)


def predict_customer(customer):
    customer_df = pd.DataFrame([customer])

    # Ensure same columns/order used during training
    customer_df = customer_df[model_features]

    probability = model.predict_proba(customer_df)[0, 1]

    risk_level = assign_risk(probability)

    recommendation = recommend_action(
        customer,
        risk_level
    )

    return {
        "churn_probability": round(float(probability), 4),
        "churn_probability_pct": round(float(probability) * 100, 1),
        "risk_level": risk_level,
        "recommended_action": recommendation
    }


# Test the function
if __name__ == "__main__":

    test_customer = {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 5,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 89.50,
        "TotalCharges": 447.50
    }

    result = predict_customer(test_customer)

    print(result)