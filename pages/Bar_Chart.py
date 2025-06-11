import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline

# Load Hugging Face model pipeline
@st.cache_resource  # Cache the model to avoid reloading it every time
def load_model():
 return pipeline("text-generation", model="distilgpt2")  # Using DistilGPT-2 for efficiency

model = load_model()

# Function to get AI-generated insights
def get_insights_from_ai(chart_data):
 """
 Generate insights using Hugging Face Transformers.
 """
 try:
     # Prepare the input text for the model
     prompt = f"""
     Analyze the following bar chart data and provide insights:
     {chart_data.to_string(index=False)}
     """

     # Generate insights using the Hugging Face model
     response = model(prompt, max_length=100, num_return_sequences=1)
     return response[0]["generated_text"]
 except Exception as e:
     return f"Error generating insights: {e}"

# Bar Chart Page
st.title("Bar Chart Visualization")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
 df = pd.read_csv(uploaded_file)
 st.write("### Dataset Preview")
 st.dataframe(df.head())

 x_column = st.selectbox("Select X-axis column:", df.columns)
 y_column = st.selectbox("Select Y-axis column:", df.columns)
 aggregation = st.selectbox(
     "Select aggregation method for Y-axis:",
     ["sum", "count", "distinct-count", "average", "max", "min"]
 )

 if st.button("Generate Bar Chart"):
     # Apply aggregation
     if aggregation == "sum":
         chart_data = df.groupby(x_column)[y_column].sum().reset_index()
     elif aggregation == "count":
         chart_data = df.groupby(x_column).size().reset_index(name="count")
         y_column = "count"
     elif aggregation == "distinct-count":
         chart_data = df.groupby(x_column)[y_column].nunique().reset_index()
     elif aggregation == "average":
         chart_data = df.groupby(x_column)[y_column].mean().reset_index()
     elif aggregation == "max":
         chart_data = df.groupby(x_column)[y_column].max().reset_index()
     elif aggregation == "min":
         chart_data = df.groupby(x_column)[y_column].min().reset_index()

     # Create bar chart
     fig = px.bar(chart_data, x=x_column, y=y_column, title=f"Bar Chart of {y_column} by {x_column}")
     st.plotly_chart(fig)

     # Generate AI Insights
     st.write("### AI-Generated Insights")
     insights = get_insights_from_ai(chart_data)
     st.write(insights)
else:
 st.info("Please upload a CSV file to get started.")
