import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Credit Risk RAG Explainer", layout="wide")
st.title("📊 Credit Risk Assessment Assistant")

csv_file = st.file_uploader("Upload a CSV of customer financials", type=["csv"])

if csv_file:
    df = pd.read_csv(csv_file)
    st.write("Preview of Uploaded Data:")
    st.dataframe(df)

    selected_row = st.selectbox("Select a customer row", df.index)
    selected_customer = df.iloc[selected_row].to_dict()

    st.subheader("Selected Customer Profile:")
    st.json(selected_customer)

    if st.button("Generate Risk Explanation"):
        response = requests.post("http://localhost:8000/rationale_from_dict", json=selected_customer)
        if response.status_code == 200:
            st.success("✅ Rationale Generated")
            st.write(response.json()["rationale"])
        else:
            st.error("❌ Failed to generate rationale. Check backend.")
