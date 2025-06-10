import streamlit as st
from transformers import pipeline

# Load the Hugging Face model pipeline
@st.cache_resource  # Cache the model to avoid reloading it every time
def load_model():
 return pipeline("text-generation", model="gpt2")  # Using GPT-2 as an example

# Initialize the model
model = load_model()

# Streamlit App
st.title("Free AI-Powered Dashboard")

# Step 1: File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
 import pandas as pd
 df = pd.read_csv(uploaded_file)
 st.write("### Dataset Preview")
 st.dataframe(df.head())

 # Step 2: Prompt Input
 st.write("### Enter Your Prompt")
 user_prompt = st.text_area(
     "Describe the dashboard or visualization you'd like to create (e.g., 'Create a bar chart of sales by region')."
 )

 if st.button("Generate Response"):
     if user_prompt.strip() == "":
         st.error("Please enter a valid prompt.")
     else:
         # Generate a response using the Hugging Face model
         with st.spinner("Generating response..."):
             response = model(user_prompt, max_length=100, num_return_sequences=1)
             generated_text = response[0]["generated_text"]

         # Display the generated response
         st.write("### Generated Response")
         st.write(generated_text)

else:
 st.info("Please upload a CSV file to get started.")

# Footer
st.markdown("---")
st.markdown("**Powered by Streamlit & Hugging Face Transformers**")
