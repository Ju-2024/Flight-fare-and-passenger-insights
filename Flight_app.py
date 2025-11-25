import streamlit as st
import joblib
import os
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.exceptions import NotFittedError

# Load trained models
model = joblib.load("flight_price_model.pkl")
sentiment_model = joblib.load("sentiment_analysis.pkl")

# Set page configuration FIRST
st.set_page_config(page_title="Flight Fare Predictor", page_icon="✈️", layout="centered")

# Custom styles
st.markdown("""
    <style>
        body {
            background-color: #e6f2ff;
        }
        .stApp {
            background-color: #e6f2ff;
        }
        .stButton>button {
            background-color: #3399ff;
            color: white;
            font-weight: bold;
        }
        .stRadio > div {
            background-color: #f0f8ff;
            border-radius: 10px;
            padding: 10px;
        }
        .stSelectbox > div {
            background-color: #f0f8ff;
            border-radius: 10px;
            padding: 5px;
        }
        .stSlider {
            padding-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Title section
st.markdown("## ✈️ Flight Fare Predictor")
st.caption("Predict your airfare and analyze airline feedback 🧳")

# Sidebar: Route Selection
st.sidebar.markdown("### 🗺️ Route Info")
from_city = st.sidebar.selectbox("🛫 From City", ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai'])
to_city = st.sidebar.selectbox("🛬 To City", ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai'])

if from_city == to_city:
    st.sidebar.error("⚠️ Source and destination cannot be the same.")

# Flight input form
st.markdown("### 🧾 Flight Details")
col1, col2 = st.columns([2, 1])
with col1:
    airline = st.selectbox("✈️ Select Airline", ['Indigo', 'SpiceJet', 'AirAsia', 'GO_FIRST', 'Vistara', 'Air_India'])
with col2:
    travel_class = st.radio("🎟️ Travel Class", ['Economy', 'Business'], horizontal=True)

days_left = st.slider("📅 Days Left Until Departure", min_value=0, max_value=60, value=30)

# Prediction button
if st.button("🎯 Predict Fare"):
    if from_city == to_city:
        st.error("Please choose different cities for departure and arrival.")
    else:
        input_df = pd.DataFrame({
            'airline': [airline],
            'class': [travel_class],
            'days_left': [days_left]
        })
        predicted_price = model.predict(input_df)[0]
        st.success(f"💸 Estimated Flight Price: ₹{predicted_price:,.2f}")

        # Fare trend chart based on days_left
        st.subheader("📈 Fare Trend by Days Left")
        trend_df = pd.DataFrame({
            'airline': [airline]*61,
            'class': [travel_class]*61,
            'days_left': list(range(0, 61))
        })
        trend_df['predicted_price'] = model.predict(trend_df)

        plt.figure(figsize=(10, 4))
        sns.lineplot(data=trend_df, x='days_left', y='predicted_price', marker='o', color='teal')
        plt.title(f"Predicted Price Trend for {airline} ({travel_class})")
        plt.xlabel("Days Left Until Departure")
        plt.ylabel("Predicted Price (₹)")
        plt.grid(True)
        st.pyplot(plt.gcf())
# --- Refund Eligibility Section ---
st.header("💸 Check Refund Policy")

# Load refund dataset
file_path = r"C:\\Users\\julis\\Downloads\\Flight_Refund.csv"
df = pd.read_csv(file_path)
df['Days Left'] = df['Hours Left'] / 24

# Refund logic function
def refund_by_days(days):
    if days > 3:
        return 'Full Refund'
    elif 1 <= days <= 3:
        return '50% Refund'
    elif 0 <= days < 1:
        return 'No Refund'
    else:
        return 'Invalid'

# Add refund status column
df['Refund by Days'] = df['Days Left'].apply(refund_by_days)

# --- Streamlit User Interaction ---
days_input = st.slider("📆 Days Left Before Departure", min_value=0, max_value=10, value=3)

if st.button("Check Refund Eligibility"):
    refund_result = refund_by_days(days_input)

    if refund_result == 'Full Refund':
        st.success(f"✅ You are eligible for a **{refund_result}**")
    elif refund_result == '50% Refund':
        st.warning(f"🔁 You are eligible for a **{refund_result}**")
    elif refund_result == 'No Refund':
        st.error(f"❌ Sorry, you're eligible for **{refund_result}**")
    else:
        st.info("Invalid input or data")

# Airline Recommendation Review Block
if st.button("📊 Customer Reviews on This Airline"):
    try:
        # Load airline review dataset to calculate recommendation rate
        review_path = os.path.join("C:\\Users\\julis\\Downloads", "Indian_Domestic_Airline.csv")
        review_data = pd.read_csv(review_path)
        airline_reviews = review_data[review_data["AirLine_Name"] == airline]

        if not airline_reviews.empty:
            total_reviews = len(airline_reviews)
            recommended = airline_reviews["Recommond"].str.lower().eq("yes").sum()
            not_recommended = total_reviews - recommended
            recommend_percent = round((recommended / total_reviews) * 100, 1)

            # Show recommendation result
            if recommend_percent >= 70:
                st.success(f"👍 {recommend_percent}% of customers recommend **{airline}**. Good to go!")
            else:
                st.warning(f"⚠️ Only {recommend_percent}% of customers recommend **{airline}**. Consider choosing another airline.")

            # Add pie chart visualization
            fig, ax = plt.subplots()
            ax.pie([recommended, not_recommended], labels=['Recommended', 'Not Recommended'],
                   autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF7043'])
            ax.axis('equal')
            plt.title(f"Customer Recommendation Breakdown for {airline}")
            st.pyplot(fig)
        else:
            st.info("ℹ️ No review data available for this airline.")
    except Exception as e:
        st.error(f"❌ Could not load review data: {str(e)}")
# --- In-flight Meal Options ---
st.header("🍽️ In-flight Meal Options")

# Default selected airline (from ticket info)
selected_airline = "Indigo"  # This should ideally be passed from ticket booking context

meal_data = {
    "Indigo": [
        {"Item": "Vegetable Biryani", "Price": 140, "Veg": True, "Type": "Meal"},
        {"Item": "Sambar Sadam", "Price": 120, "Veg": True, "Type": "Meal"},
        {"Item": "Lemon Rice", "Price": 110, "Veg": True, "Type": "Meal"},
        {"Item": "Paneer Butter Masala & Rice", "Price": 160, "Veg": True, "Type": "Meal"},
        {"Item": "Mix Veg Curry with Roti", "Price": 140, "Veg": True, "Type": "Meal"},
        {"Item": "Veg Puff", "Price": 45, "Veg": True, "Type": "Snack"},
        {"Item": "Chicken Biryani", "Price": 170, "Veg": False, "Type": "Meal"},
        {"Item": "Chicken Curry & Rice", "Price": 165, "Veg": False, "Type": "Meal"},
        {"Item": "Egg Fried Rice", "Price": 130, "Veg": False, "Type": "Meal"},
        {"Item": "Fish Biryani", "Price": 175, "Veg": False, "Type": "Meal"},
        {"Item": "Chicken 65", "Price": 95, "Veg": False, "Type": "Snack"},
        {"Item": "Mutton Keema Roll", "Price": 150, "Veg": False, "Type": "Snack"},
    ],
    "AirAsia": [
        {"Item": "Paneer Wrap", "Price": 120, "Veg": True, "Type": "Meal"},
        {"Item": "Vegetable Pulao", "Price": 130, "Veg": True, "Type": "Meal"},
        {"Item": "Aloo Paratha with Curd", "Price": 120, "Veg": True, "Type": "Meal"},
        {"Item": "Chole Bhature", "Price": 135, "Veg": True, "Type": "Meal"},
        {"Item": "Masala Corn", "Price": 35, "Veg": True, "Type": "Snack"},
        {"Item": "Samosa", "Price": 40, "Veg": True, "Type": "Snack"},
        {"Item": "Chicken Curry", "Price": 150, "Veg": False, "Type": "Meal"},
        {"Item": "Mutton Biryani", "Price": 190, "Veg": False, "Type": "Meal"},
        {"Item": "Prawn Pulao", "Price": 180, "Veg": False, "Type": "Meal"},
        {"Item": "Egg Bhurji Sandwich", "Price": 85, "Veg": False, "Type": "Snack"},
        {"Item": "Fish Cutlet", "Price": 85, "Veg": False, "Type": "Snack"},
        {"Item": "Chicken Sausage Roll", "Price": 90, "Veg": False, "Type": "Snack"},
    ],
    "Vistara": [
        {"Item": "Rajma Chawal", "Price": 130, "Veg": True, "Type": "Meal"},
        {"Item": "Coconut Rice", "Price": 115, "Veg": True, "Type": "Meal"},
        {"Item": "Mint Rice", "Price": 110, "Veg": True, "Type": "Meal"},
        {"Item": "Grilled Veg Sandwich", "Price": 85, "Veg": True, "Type": "Snack"},
        {"Item": "Khakhra", "Price": 30, "Veg": True, "Type": "Snack"},
        {"Item": "Fruit Salad", "Price": 60, "Veg": True, "Type": "Snack"},
        {"Item": "Egg Biryani", "Price": 140, "Veg": False, "Type": "Meal"},
        {"Item": "Chettinad Chicken Rice", "Price": 180, "Veg": False, "Type": "Meal"},
        {"Item": "Fish Fry & Rice", "Price": 190, "Veg": False, "Type": "Meal"},
        {"Item": "Prawn Cutlet", "Price": 95, "Veg": False, "Type": "Snack"},
        {"Item": "Chicken Nuggets", "Price": 85, "Veg": False, "Type": "Snack"},
        {"Item": "Chicken Samosa", "Price": 50, "Veg": False, "Type": "Snack"},
    ],
    "Air India": [
        {"Item": "Curd Rice", "Price": 100, "Veg": True, "Type": "Meal"},
        {"Item": "Palak Paneer with Roti", "Price": 140, "Veg": True, "Type": "Meal"},
        {"Item": "Paneer Fried Rice", "Price": 130, "Veg": True, "Type": "Meal"},
        {"Item": "Masala Dosa", "Price": 95, "Veg": True, "Type": "Meal"},
        {"Item": "Thattai", "Price": 30, "Veg": True, "Type": "Snack"},
        {"Item": "Cashew Pack", "Price": 60, "Veg": True, "Type": "Snack"},
        {"Item": "Chicken Curry & Rice", "Price": 160, "Veg": False, "Type": "Meal"},
        {"Item": "Prawn Biryani", "Price": 190, "Veg": False, "Type": "Meal"},
        {"Item": "Ambur Mutton Biryani", "Price": 195, "Veg": False, "Type": "Meal"},
        {"Item": "Grilled Fish Sandwich", "Price": 120, "Veg": False, "Type": "Snack"},
        {"Item": "Mutton Puff", "Price": 65, "Veg": False, "Type": "Snack"},
        {"Item": "Boiled Egg", "Price": 25, "Veg": False, "Type": "Snack"},
    ]
}

# --- Business Class Specials ---
business_class_specials = {
    "Indigo": [
        {"Item": "Paneer Tikka Masala with Jeera Rice", "Price": 200, "Veg": True, "Type": "Meal"},
        {"Item": "Grilled Veg Lasagna", "Price": 210, "Veg": True, "Type": "Meal"},
        {"Item": "Methi Mutter Malai", "Price": 180, "Veg": True, "Type": "Meal"},
        {"Item": "Almond Brownie", "Price": 70, "Veg": True, "Type": "Snack"},
        {"Item": "Cheese Cubes", "Price": 50, "Veg": True, "Type": "Snack"},
        {"Item": "Butter Chicken with Naan", "Price": 240, "Veg": False, "Type": "Meal"},
        {"Item": "Mutton Rogan Josh", "Price": 260, "Veg": False, "Type": "Meal"},
        {"Item": "Fish Tikka", "Price": 220, "Veg": False, "Type": "Meal"},
        {"Item": "Chicken Seekh Kabab", "Price": 90, "Veg": False, "Type": "Snack"},
        {"Item": "Egg Roll", "Price": 80, "Veg": False, "Type": "Snack"},
    ],
    "AirAsia": [
        {"Item": "Veg Pasta Alfredo", "Price": 210, "Veg": True, "Type": "Meal"},
        {"Item": "Stuffed Capsicum Rice", "Price": 200, "Veg": True, "Type": "Meal"},
        {"Item": "Cheese Garlic Bread", "Price": 85, "Veg": True, "Type": "Snack"},
        {"Item": "Premium Coffee", "Price": 50, "Veg": True, "Type": "Snack"},
        {"Item": "Fruit Tart", "Price": 60, "Veg": True, "Type": "Snack"},
        {"Item": "Malabar Chicken Biryani", "Price": 230, "Veg": False, "Type": "Meal"},
        {"Item": "Fish Molee with Appam", "Price": 250, "Veg": False, "Type": "Meal"},
        {"Item": "Chicken Manchurian Rice", "Price": 220, "Veg": False, "Type": "Meal"},
        {"Item": "Mutton Cutlet", "Price": 90, "Veg": False, "Type": "Snack"},
        {"Item": "Egg Puff", "Price": 70, "Veg": False, "Type": "Snack"},
    ],
    "Vistara": [
        {"Item": "Grilled Cottage Cheese Steak", "Price": 220, "Veg": True, "Type": "Meal"},
        {"Item": "Vegetable Cannelloni", "Price": 230, "Veg": True, "Type": "Meal"},
        {"Item": "Stuffed Kulcha & Dal Makhani", "Price": 210, "Veg": True, "Type": "Meal"},
        {"Item": "Fruit & Nut Bar", "Price": 55, "Veg": True, "Type": "Snack"},
        {"Item": "Mini Idli Fry", "Price": 65, "Veg": True, "Type": "Snack"},
        {"Item": "Tandoori Chicken & Pulao", "Price": 250, "Veg": False, "Type": "Meal"},
        {"Item": "Lamb Rogan Josh with Rice", "Price": 260, "Veg": False, "Type": "Meal"},
        {"Item": "Fish Curry with Steamed Rice", "Price": 240, "Veg": False, "Type": "Meal"},
        {"Item": "Chicken Samosa", "Price": 60, "Veg": False, "Type": "Snack"},
        {"Item": "Boiled Egg with Salt & Pepper", "Price": 30, "Veg": False, "Type": "Snack"},
    ],
    "Air India": [
        {"Item": "Palak Paneer with Jeera Rice", "Price": 210, "Veg": True, "Type": "Meal"},
        {"Item": "Paneer Tikka Roll", "Price": 180, "Veg": True, "Type": "Snack"},
        {"Item": "Dal Makhani & Roti", "Price": 200, "Veg": True, "Type": "Meal"},
        {"Item": "Lassi", "Price": 40, "Veg": True, "Type": "Snack"},
        {"Item": "Dry Fruit Ladoo", "Price": 65, "Veg": True, "Type": "Snack"},
        {"Item": "Butter Garlic Prawns", "Price": 270, "Veg": False, "Type": "Meal"},
        {"Item": "Chicken Korma with Rice", "Price": 250, "Veg": False, "Type": "Meal"},
        {"Item": "Mutton Korma with Ghee Rice", "Price": 250, "Veg": False, "Type": "Meal"},
        {"Item": "Chicken Cutlet", "Price": 85, "Veg": False, "Type": "Snack"},
        {"Item": "Egg Curry", "Price": 100, "Veg": False, "Type": "Meal"},
    ]
}

# --- Seasonal Menu ---
seasonal_menu = [
    {"Item": "Mango Kulfi", "Price": 50, "Veg": True, "Type": "Snack"},
    {"Item": "Summer Salad with Mint Dressing", "Price": 70, "Veg": True, "Type": "Snack"},
    {"Item": "Jackfruit Biryani", "Price": 160, "Veg": True, "Type": "Meal"}
]

# --- Streamlit UI Logic ---
#st.title("🌟 In-Flight Meal Selector")
#selected_airline = st.selectbox("Select Airline:", list(meal_data.keys()))
veg_filter = st.radio("Meal Preference:", options=["All", "Veg", "Non-Veg", "Snacks Only"])
travel_class = st.radio("Class:", options=["Economy", "Business"])
include_seasonal = st.checkbox("Include Seasonal Menu?")
selected_meals = []

# --- Combine Menus ---
all_meals = meal_data[selected_airline].copy()
if travel_class == "Business":
    all_meals += business_class_specials.get(selected_airline, [])
if include_seasonal:
    all_meals += seasonal_menu

# --- Display Menu ---
st.write("### Menu:")
for meal in all_meals:
    if veg_filter == "Veg" and (not meal.get("Veg", True) or meal.get("Type") == "Snack"):
        continue
    if veg_filter == "Non-Veg" and (meal.get("Veg", True) or meal.get("Type") == "Snack"):
        continue
    if veg_filter == "Snacks Only" and meal.get("Type") != "Snack":
        continue

    if st.checkbox(f"{meal['Item']} - ₹{meal['Price']} ({travel_class})", key=f"{selected_airline}_{meal['Item']}_{travel_class}"):
        selected_meals.append(meal)

# --- Total Price Calculation ---
meal_total = sum(m['Price'] for m in selected_meals)
if selected_meals:
    st.success(f"**Total Meal Cost: ₹{meal_total}**")
else:
    st.info("Select items to view total.")
