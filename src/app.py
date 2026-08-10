from flask import Flask, request, render_template
from predict import predict_customer
from ollama_explainer import explain_customer

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    ai_explanation = None

    if request.method == "POST":
        customer_data = {
            "gender": request.form["gender"],
            "SeniorCitizen": int(request.form["SeniorCitizen"]),
            "Partner": request.form["Partner"],
            "Dependents": request.form["Dependents"],
            "tenure": int(request.form["tenure"]),
            "PhoneService": request.form["PhoneService"],
            "MultipleLines": request.form["MultipleLines"],
            "InternetService": request.form["InternetService"],
            "OnlineSecurity": request.form["OnlineSecurity"],
            "OnlineBackup": request.form["OnlineBackup"],
            "DeviceProtection": request.form["DeviceProtection"],
            "TechSupport": request.form["TechSupport"],
            "StreamingTV": request.form["StreamingTV"],
            "StreamingMovies": request.form["StreamingMovies"],
            "Contract": request.form["Contract"],
            "PaperlessBilling": request.form["PaperlessBilling"],
            "PaymentMethod": request.form["PaymentMethod"],
            "MonthlyCharges": float(request.form["MonthlyCharges"]),
            "TotalCharges": float(request.form["TotalCharges"])
        }

        result = predict_customer(customer_data)

        ai_explanation = explain_customer(
            customer_data,
            result
        )

    return render_template(
        "index.html",
        result=result,
        ai_explanation=ai_explanation
    )


if __name__ == "__main__":
    app.run(debug=True)