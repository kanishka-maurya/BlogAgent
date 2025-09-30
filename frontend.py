import streamlit as st
import requests
import json


st.header("BlogAgent")
API_URL = "http://localhost:8000/generate-blog"


topic = st.text_input("Enter the blog topic", "The Future of AI in Healthcare")
target_length = st.number_input("Target Length", min_value=300, max_value=5000, value=1000, step=100)
style = st.text_input("Enter the writing style", "informative and engaging")

if st.button("Generate Blog"):

    input_data = {
        "topic":topic,
        "target_length":target_length,
        "style":style
    }
    
    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200 and "response" in result:
           st.write(result["response"])

        else:
            st.error(f"Status: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")