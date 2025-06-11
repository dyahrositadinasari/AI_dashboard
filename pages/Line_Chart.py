import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline

# Load Hugging Face summarization model
@st.cache_resource  # Cache the model to avoid reloading it every time
def load_model():
 return pipeline("summarization", model="facebook/bart-large-cnn")  # Using BART for summarization

model = load_model()

# Function to preprocess chart data into key statistics
def preprocess_chart_data(chart_data):
 """
 Extract key statistics from the chart data to provide meaningful insights.
 """
 summary = {}
 summary["highest_x"] = chart_data.iloc[chart_data.iloc[:, 1].idxmax(), 0]
 summary["highest_y"] = chart_data.iloc[:, 1].max()
 summary["lowest_x"] = chart_data.iloc[chart_data.iloc[:, 1].idxmin(), 0]
 summary["lowest_y"] = chart_data.iloc[:, 1].min()
 summary["average_y"] = chart_data.iloc[:, 1].mean()
 return summary

# Function to get AI-generated insights
def get_insights_from_ai(preprocessed_summary):
 """
 Generate insights using Hugging Face Transformers.
 """
 try:
     # Prepare the input text for the model
     prompt = f"""
     Analyze the following line chart summary and provide key insights:
     - Highest value: {preprocessed_summary['highest_y']} at {preprocessed_summary['highest_x']}
     - Lowest value: {preprocessed_summary['lowest_y']} at {preprocessed_summary['lowest_x']}
     - Average value: {preprocessed_summary['average_y']}
     """

     # Generate insights using the Hugging Face model
     response = model(prompt, max_length=100, min_length=30, num_return_sequences=1)
     return response[0]["summary_text"]
 except Exception as e:
     return f"Error generating insights: {e}"

# Line Chart Page
st.title("Line Chart Visualization")

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

 if st.button("Generate Line Chart"):
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

     # Create line chart
     fig = px.line(chart_data, x=x_column, y=y_column, title=f"Line Chart of {y_column} vs {x_column}")
     st.plotly_chart(fig)

     # Preprocess chart data to extract key statistics
     preprocessed_summary = preprocess_chart_data(chart_data)

     # Generate AI Insights
     st.write("### AI-Generated Insights")
     insights = get_insights_from_ai(preprocessed_summary)
     st.write(insights)
else:
 st.info("Please upload a CSV file to get started.")
