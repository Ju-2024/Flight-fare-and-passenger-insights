🛫 Flight Fare & Passenger Insights Dashboard
Machine Learning • NLP • Streamlit • End-to-End Data Science Project
🛩️ Project Overview

This project provides a complete airline analytics solution featuring:

Flight fare prediction using machine learning regression models

Passenger sentiment analysis using NLP

Refund eligibility estimation using rule-based logic

In-flight meal recommendations

A unified, interactive Streamlit dashboard for real-time insights

It demonstrates strong capabilities in data preprocessing, EDA, feature engineering, model development, NLP pipelines, and deployable application design.

📁 Project Structure
.
├── Flight_Analysis.csv
├── Flight_Analysis_Capstone.ipynb
├── Flight_app.py
├── flight_price_model.pkl
├── Flight_Refund.ipynb
├── Flight_Review.csv
├── sentiment_analysis.pkl
└── requirements.txt

✨ Key Features
✈️ Flight Fare Prediction

Predicts ticket prices based on airline, route, timings, duration, and number of stops.

🙂 Sentiment Analysis (NLP)

Classifies airline review text into Positive, Neutral, or Negative using TF-IDF and Logistic Regression.

💸 Refund Eligibility Checker

Rule-based logic designed to determine ticket refundability based on user inputs.

🍱 Meal Recommendations

Provides Veg/Non-Veg meal suggestions specific to airline selection.

🎛️ Streamlit Dashboard

A clean and user-friendly interface combining all predictions in one place.

🧠 Project Architecture
                 ┌───────────────────┐
                 │   Flight Dataset  │
                 └──────────┬────────┘
                            │
                 ┌──────────▼──────────┐
                 │ EDA + Feature Engg. │
                 └──────────┬──────────┘
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
┌──────▼──────┐     ┌──────▼───────┐     ┌──────▼────────┐
│ Fare Model  │     │ Sentiment    │     │ Refund Logic   │
│ Regression  │     │ NLP Model    │     │ Rule-based     │
└──────┬──────┘     └──────┬───────┘     └──────┬────────┘
       │                    │                    │
       └──────────────┬─────┴─────┬─────────────┘
                      ▼           ▼
                 ┌─────────────────────┐
                 │ Streamlit Dashboard │
                 └─────────────────────┘

🚀 How to Run the App
1. Install dependencies
pip install -r requirements.txt

2. Launch the Streamlit app
streamlit run Flight_app.py

🔧 Tech Stack

Python

Pandas, NumPy

Scikit-Learn

Streamlit

NLTK

Matplotlib & Seaborn

Joblib

📊 Model Components
Fare Prediction

Random Forest, Extra Trees, and Gradient Boosting models
Saved model → flight_price_model.pkl

Sentiment Analysis

TF-IDF Vectoriser + Logistic Regression
Saved model → sentiment_analysis.pkl

Refund Logic

Custom rule-based system
Notebook → Flight_Refund.ipynb

🌟 Future Enhancements

Integrate real-time flight price APIs

Expand meal recommendation dataset

Add deep-learning sentiment model

Deploy on AWS / Azure / Streamlit Cloud

👩‍💻 Author

Julisha Pushparaj
Sydney, Australia
Data Analyst & Machine Learning Enthusiast
