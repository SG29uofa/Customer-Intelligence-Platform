import subprocess
import re


def explain_customer(customer, result):

    prompt = f"""
You are an AI explanation layer for a customer churn analytics system.

Your job is ONLY to summarize the facts supplied below.
Do not make predictions yourself.
Do not add facts, assumptions, causes, time periods, business outcomes,
customer motivations, satisfaction claims, or financial claims.

MODEL RESULT
Predicted churn probability: {result['churn_probability_pct']}%
Risk classification: {result['risk_level']}

CUSTOMER PROFILE
Tenure: {customer['tenure']} months
Contract: {customer['Contract']}
Internet service: {customer['InternetService']}
Tech Support: {customer['TechSupport']}
Online Security: {customer['OnlineSecurity']}
Payment Method: {customer['PaymentMethod']}
Monthly Charges: ${customer['MonthlyCharges']}

VALIDATED ANALYTICAL FINDINGS FROM THE HISTORICAL DATA
- Shorter-tenure customers showed higher observed churn rates.
- Month-to-month customers showed higher observed churn rates than
  one-year and two-year contract customers.
- Fiber-optic customers showed higher observed churn rates than DSL
  customers in this dataset.
- Customers without Tech Support showed higher observed churn rates
  than customers with Tech Support.
- Customers without Online Security showed higher observed churn rates
  than customers with Online Security.
- Electronic-check customers showed higher observed churn rates than
  customers using the other payment methods analyzed.
- These are associations only. They do NOT establish causation.

RULE-BASED RETENTION ACTIONS
{result['recommended_action']}

STRICT RULES
1. Never invent a churn time horizon.
2. Never say "next 30 days", "next 6 months", or any similar time period.
3. Never describe the customer as valuable, profitable, loyal, dissatisfied,
   unhappy, or having problems unless explicitly provided.
4. Never say a feature causes churn.
5. Never say an intervention will prevent churn.
6. Never introduce recommendations that are not listed above.
7. Do not describe any supplied high-risk characteristic as a low-risk factor.
8. Use phrases such as "was associated with higher observed churn in the
   historical data."
9. Keep the entire response below 110 words.

Return exactly these two sections:

Risk Explanation:
In 2-3 sentences, explain the model result using only the customer profile
and validated analytical findings above.

Suggested Retention Actions:
In 1-2 sentences, summarize only the rule-based actions supplied above.
"""

    process = subprocess.run(
        ["ollama", "run", "llama3.2"],
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8"
    )

    if process.returncode != 0:
        return f"Ollama error: {process.stderr}"

    output = process.stdout
    # Remove ANSI / terminal control characters
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    output = ansi_escape.sub('', output)
    return output.strip()


# Standalone test
if __name__ == "__main__":

    test_customer = {
        "tenure": 5,
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic",
        "TechSupport": "No",
        "OnlineSecurity": "No",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 89.50
    }

    test_result = {
        "churn_probability_pct": 75.7,
        "risk_level": "High",
        "recommended_action":
            "Priority retention outreach | "
            "Review longer-term contract incentive | "
            "Review Tech Support offer | "
            "Review Online Security offer | "
            "Review automatic payment incentive"
    }

    explanation = explain_customer(
        test_customer,
        test_result
    )

    print(explanation)