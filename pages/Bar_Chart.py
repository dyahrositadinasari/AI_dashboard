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
 summary["highest_category"] = chart_data.iloc[chart_data.iloc[:, 1].idxmax(), 0]
 summary["highest_value"] = chart_data.iloc[:, 1].max()
 summary["lowest_category"] = chart_data.iloc[chart_data.iloc[:, 1].idxmin(), 0]
 summary["lowest_value"] = chart_data.iloc[:, 1].min()
 summary["total_sum"] = chart_data.iloc[:, 1].sum()
 summary["average_value"] = chart_data.iloc[:, 1].mean()
 return summary

def get_insights_from_ai(preprocessed_summary):
 try:
  print("Preprocessed Summary:", preprocessed_summary)
  # Prepare the input text for the model
  prompt = f"""
  Analyze the following bar chart summary and provide key insights:
  - Highest category: {preprocessed_summary['highest_category']} ({preprocessed_summary['highest_value']})
  - Lowest category: {preprocessed_summary['lowest_category']} ({preprocessed_summary['lowest_value']})
  - Total sum: {preprocessed_summary['total_sum']}
  - Average value: {preprocessed_summary['average_value']}
  """
  # Debugging: Print the generated prompt
  print("Generated Prompt:", prompt)

  # Generate insights using the Hugging Face model
  response = model(prompt, max_length=100, min_length=30, num_return_sequences=1)

  # Debugging: Print the raw response
  print("Raw Response:", response)

  # Extract and return the summary text
  if isinstance(response, list) and "summary_text" in response[0]:
   return response[0]["summary_text"]
  else:
   return "Unexpected response format from the model."
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

     # Preprocess chart data to extract key statistics
     preprocessed_summary = preprocess_chart_data(chart_data)

     # Generate AI Insights
     st.write("### AI-Generated Insights")
     insights = get_insights_from_ai(preprocessed_summary)
     st.write(insights)
else:
 st.info("Please upload a CSV file to get started.")
