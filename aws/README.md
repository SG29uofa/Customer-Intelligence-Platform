# AWS SageMaker Extension

This folder contains the AWS cloud extension of the Customer Intelligence Platform.

The objective was to reproduce a customer churn machine-learning workflow in AWS using Amazon S3 for cloud storage and Amazon SageMaker Studio for model development and evaluation.

## Architecture

Amazon S3  
↓  
SageMaker Studio / JupyterLab  
↓  
Load Customer Dataset from S3  
↓  
Data Cleaning & Preprocessing  
↓  
Stratified Train/Test Split  
↓  
Scikit-learn Pipeline  
↓  
Logistic Regression Training  
↓  
Model Evaluation  
↓  
Serialized Model Artifact  
↓  
Amazon S3 Model Storage

## Dataset

The IBM Telco Customer Churn dataset was stored in Amazon S3 and accessed directly from the SageMaker environment using Boto3.

Dataset dimensions:

- 7,043 customers
- 21 original columns
- Binary target: `Churn`

## AWS Workflow

The SageMaker notebook performs the following steps:

1. Connects to Amazon S3 using Boto3.
2. Loads the churn dataset directly from the S3 bucket.
3. Cleans and prepares the customer data.
4. Creates a stratified training and test split.
5. Builds a Scikit-learn preprocessing and Logistic Regression pipeline.
6. Trains the model inside the SageMaker JupyterLab environment.
7. Evaluates the model on the held-out test set.
8. Serializes the trained pipeline using Joblib.
9. Stores the model artifact in Amazon S3.

## Model Results

The AWS Logistic Regression pipeline achieved the following results on the held-out test set:

| Metric | Result |
|---|---:|
| Accuracy | 80.88% |
| Precision | 66.67% |
| Recall | 55.97% |
| F1 Score | 60.85% |
| ROC-AUC | **0.8448** |

Confusion matrix:

```text
[[1395, 157],
 [ 247, 314]]
