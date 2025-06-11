import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline

@st.cache_resource
def load_model():
  return pipeline("text2text-generation", model="google/flan-t5-base")

model = load_model()

def preprocess_chart_data(chart_data):
  summary = {}
  summary["highest_x"] = chart_data.iloc[chart_data.iloc[:, 1].idxmax(), 0]
  summary["highest_y"] = chart_data.iloc[:, 1].max()
  summary["lowest_x"] = chart_data.iloc[chart_data.iloc[:, 1].idxmin(), 0]
  summary["lowest_y"] = chart_data.iloc[:, 1].min()
  summary["average_y"] = chart_data.iloc[:, 1].mean()
  return summary

def get_insights_from_ai(preprocessed_summary):
  try:
      prompt = f"""
      Analyze the following line chart summary and provide key insights:
      - The highest value is {preprocessed_summary['highest_y']} at {preprocessed_summary['highest_x']}.
      - The lowest value is {preprocessed_summary['lowest_y']} at {preprocessed_summary['lowest_x']}.
      - The average value is {preprocessed_summary['average_y']}.
      """
      response = model(prompt, max_length=100, num_return_sequences=1)
      return response[0]["generated_text"]
  except Exception as e:
      return f"Error generating insights: {e}"

st.title("Line Chart Visualization")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)

  # Ensure that any date columns are parsed correctly
  for col in df.columns:
      if "date" in col.lower():  # Identify potential date columns by name
          try:
              df[col] = pd.to_datetime(df[col], errors="coerce")  # Handle invalid dates
              df = df.dropna(subset=[col])  # Drop rows with invalid dates
          except Exception as e:
              st.warning(f"Could not parse column '{col}' as dates: {e}")

  st.write("### Dataset Preview")
  st.dataframe(df.head())

  x_column = st.selectbox("Select X-axis column:", df.columns)
  y_column = st.selectbox("Select Y-axis column:", df.columns)

  # Ensure Y-axis column is numeric
  if not pd.api.types.is_numeric_dtype(df[y_column]):
      st.error(f"The selected Y-axis column '{y_column}' must contain numeric data.")
      st.stop()

  aggregation = st.selectbox(
      "Select aggregation method for Y-axis:",
      ["sum", "count", "distinct-count", "average", "max", "min"]
  )

  if pd.api.types.is_datetime64_any_dtype(df[x_column]):
      group_by_date = st.selectbox(
          "Group dates by:",
          ["None", "Date", "Month", "Year", "Year-Month"]
      )
  else:
      group_by_date = "None"

  if st.button("Generate Line Chart"):
      if group_by_date == "Date":
          df["Date"] = df[x_column].dt.date
          x_column = "Date"
      elif group_by_date == "Month":
          df["Month"] = df[x_column].dt.month_name()
          x_column = "Month"
      elif group_by_date == "Year":
          df["Year"] = df[x_column].dt.year
          x_column = "Year"
      elif group_by_date == "Year-Month":
          df["Year-Month"] = df[x_column].dt.to_period("M").astype(str)
          x_column = "Year-Month"

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

      fig = px.line(chart_data, x=x_column, y=y_column, title=f"Line Chart of {y_column} vs {x_column}")
      st.plotly_chart(fig)

      preprocessed_summary = preprocess_chart_data(chart_data)
      insights = get_insights_from_ai(preprocessed_summary)
      st.write("### AI-Generated Insights")
      st.write(insights)
else:
  st.info("Please upload a CSV file to get started.")
