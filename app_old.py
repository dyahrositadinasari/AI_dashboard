import streamlit as st
import pandas as pd
from transformers import pipeline
import matplotlib.pyplot as plt
import plotly.express as px

# Load the Hugging Face model pipeline
@st.cache_resource  # Cache the model to avoid reloading it every time
def load_model():
 return pipeline("text-generation", model="gpt2")  # Using GPT-2 as an example

# Initialize the model
model = load_model()

# Streamlit App
st.title("Free AI-Powered Dashboard v.2.0")

# Step 1: File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
 # Load the dataset
 df = pd.read_csv(uploaded_file)
 st.write("### Dataset Preview")
 st.dataframe(df.head())

 # Step 2: Prompt Input
 st.write("### Enter Your Prompt")
 user_prompt = st.text_area(
     "Describe the dashboard or visualization you'd like to create (e.g., 'Create a bar chart of sales by region')."
 )

 if st.button("Generate Visualization"):
     if user_prompt.strip() == "":
         st.error("Please enter a valid prompt.")
     else:
         # Generate a response using the Hugging Face model
         with st.spinner("Processing your request..."):
             response = model(user_prompt, max_length=100, num_return_sequences=1)
             generated_text = response[0]["generated_text"]

         # Display the generated response (debugging purpose)
         st.write("### Model Interpretation")
         st.write(generated_text)

         # Step 3: Parse the Prompt and Create Visualization
         try:
             if "bar chart" in user_prompt.lower():
                 # Example: Assume the user wants a bar chart grouped by a column
                 column_name = st.selectbox("Select a column for grouping:", df.columns)
                 fig = px.bar(df, x=column_name, title=f"Bar Chart of {column_name}")
                 st.plotly_chart(fig)

             elif "line chart" in user_prompt.lower():
                 # Example: Assume the user wants a line chart with two columns
                 x_column = st.selectbox("Select X-axis column:", df.columns)
                 y_column = st.selectbox("Select Y-axis column:", df.columns)
                 fig = px.line(df, x=x_column, y=y_column, title=f"Line Chart of {y_column} vs {x_column}")
                 st.plotly_chart(fig)

             elif "scatter plot" in user_prompt.lower():
                 # Example: Assume the user wants a scatter plot with two columns
                 x_column = st.selectbox("Select X-axis column:", df.columns)
                 y_column = st.selectbox("Select Y-axis column:", df.columns)
                 fig = px.scatter(df, x=x_column, y=y_column, title=f"Scatter Plot of {y_column} vs {x_column}")
                 st.plotly_chart(fig)

             else:
                 st.error("Sorry, I couldn't understand the type of visualization you want. Please refine your prompt.")

         except Exception as e:
             st.error(f"An error occurred while generating the visualization: {e}")

else:
 st.info("Please upload a CSV file to get started.")

# Footer
st.markdown("---")
st.markdown("**Powered by Streamlit & Hugging Face Transformers**")
