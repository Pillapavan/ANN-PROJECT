import streamlit as st
import numpy as np
import tensorflow as tf
import pandas as pd
import pickle

# 1. Load the trained model and unified preprocessor pipeline
model = tf.keras.models.load_model('model.h5')

with open('preprocessor.pkl', 'rb') as file:
    preprocessor = pickle.load(file)

geo_categories = ['France', 'Spain', 'Germany']

# 3. Streamlit UI Elements
st.title('Customer Churn Prediction')

st.subheader('Enter Customer Details:')
geography = st.selectbox('Geography', geo_categories)
gender = st.selectbox('Gender', ['Female', 'Male'])
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance', min_value=0.0, step=100.0)
credit_score = st.number_input('Credit Score', min_value=300, max_value=850, step=1)
estimated_salary = st.number_input('Estimated Salary', min_value=0.0, step=500.0)
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
is_active_member = st.selectbox('Is Active Member', [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

# 4. Prepare raw input DataFrame (Must exactly match the original Column names before preprocessing)
input_df = pd.DataFrame([{
    'CreditScore': credit_score,
    'Geography': geography,
    'Gender': gender,
    'Age': age,
    'Tenure': tenure,
    'Balance': balance,
    'NumOfProducts': num_of_products,
    'HasCrCard': has_cr_card,
    'IsActiveMember': is_active_member,
    'EstimatedSalary': estimated_salary
}])

# 5. Pipeline Preprocessing 
# The preprocessor automatically applies One-Hot Encoding and Scaling to the correct columns in one pass
input_data_scaled = preprocessor.transform(input_df)

# 6. Predict Churn
# 6. Predict Churn and Display a High-Quality Dashboard
if st.button('Run Risk Analysis', use_container_width=True):
    prediction = model.predict(input_data_scaled)
    prediction_proba = float(prediction[0][0])
    
    st.write('---')
    st.subheader("📊 Analysis Results")
    
    # Create clean side-by-side metric layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Display the probability like a professional KPI dashboard
        st.metric(
            label="Calculated Retention Risk", 
            value=f"{prediction_proba * 100:.1f}%",
            delta="Safe Range" if prediction_proba <= 0.5 else "Action Required",
            delta_color="normal" if prediction_proba <= 0.5 else "inverse"
        )
        
    with col2:
        st.markdown("**Account Health Summary:**")
        if prediction_proba > 0.5:
            st.error('⚠️ **High Risk Account**\n\nThis profile mimics patterns of previous customers who canceled their service. Consider proactive outreach.')
        else:
            st.success('✅ **Healthy Account Profile**\n\nThis customer shows high engagement signs. Risk of cancellation is extremely negligible.')

    # Provide business context based on the specific inputs
    st.markdown("### 🔍 Key Positive Indicators")
    bullets = []
    if is_active_member == 1:
        bullets.append("✨ **Active Membership:** Regular account usage is strongly driving down risk scores.")
    if num_of_products >= 2:
        bullets.append("📦 **Product Ecosystem:** Multi-product clients traditionally demonstrate much higher loyalty.")
    if balance > 50000:
        bullets.append("💰 **Financial Footprint:** Substantial account balance signals a highly anchored relationship.")
        
    if bullets:
        for b in bullets:
            st.markdown(b)
    else:
        st.caption("Standard baseline account activity detected.")

