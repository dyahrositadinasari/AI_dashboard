import streamlit as st
import pandas as pd
import plotly.express as px

# Function to parse user prompts and determine the type of visualization
def parse_prompt(prompt):
  """
  Parse the user's natural language prompt to identify the chart type and relevant columns.
  Returns a dictionary with 'chart_type', 'x_column', and 'y_column'.
  """
  prompt = prompt.lower()
  if "bar chart" in prompt:
      return {"chart_type": "bar"}
  elif "line chart" in prompt:
      return {"chart_type": "line"}
  elif "scatter plot" in prompt:
      return {"chart_type": "scatter"}
  else:
      return {"chart_type": None}

# Function to create a visualization based on user input
def create_visualization(df, chart_type, x_column, y_column):
  if chart_type == "bar":
      fig = px.bar(df, x=x_column, y=y_column, title=f"Bar Chart of {y_column} vs {x_column}")
  elif chart_type == "line":
      fig = px.line(df, x=x_column, y=y_column, title=f"Line Chart of {y_column} vs {x_column}")
  elif chart_type == "scatter":
      fig = px.scatter(df, x=x_column, y=y_column, title=f"Scatter Plot of {y_column} vs {x_column}")
  else:
      fig = None
  return fig

# Streamlit App
st.title("AI-Powered Dashboard (Reset Version)")

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
      "Describe the visualization you'd like to create (e.g., 'Create a bar chart of sales by region')."
  )

  if st.button("Generate Visualization"):
      if user_prompt.strip() == "":
          st.error("Please enter a valid prompt.")
      else:
          # Parse the user's prompt
          parsed_prompt = parse_prompt(user_prompt)
          chart_type = parsed_prompt["chart_type"]

          if chart_type is None:
              st.error("Sorry, I couldn't understand the type of visualization you want. Please refine your prompt.")
          else:
              # Let the user select columns for the visualization
              st.write(f"Detected chart type: {chart_type.capitalize()} Chart")
              x_column = st.selectbox("Select X-axis column:", df.columns)
              y_column = st.selectbox("Select Y-axis column:", df.columns)

              # Create and display the visualization
              fig = create_visualization(df, chart_type, x_column, y_column)
              if fig:
                  st.plotly_chart(fig)
              else:
                  st.error("An error occurred while generating the visualization.")

else:
  st.info("Please upload a CSV file to get started.")

# Footer
st.markdown("---")
st.markdown("**Powered by Streamlit & Plotly**")
