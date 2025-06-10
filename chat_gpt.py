import streamlit as st
import pandas as pd
import openai  # For GPT-4 integration
import matplotlib.pyplot as plt
import plotly.express as px
import io

# Set up OpenAI API Key
openai.api_key = st.secrets["openai_api_key"]

# Function to query OpenAI GPT-4
def query_genai(prompt):
  try:
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello! How can I use OpenAI in Streamlit?"}
    ]
    )
    print(response['choices'][0]['message']['content'])
  except Exception as e:
      return f"Error: {e}"

# Function to execute generated Python code
def execute_code(code, df):
  try:
      # Create a local variable scope for execution
      local_scope = {"df": df, "plt": plt, "px": px, "io": io}
      exec(code, {}, local_scope)
      return local_scope.get("fig", None)  # Return 'fig' if it exists
  except Exception as e:
      return f"Error executing code: {e}"

# Streamlit App
st.title("GenAI-Powered Dashboard")

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
          # Combine the user's prompt with context about the dataset
          full_prompt = (
              f"The user has uploaded a dataset with the following columns: {', '.join(df.columns)}.\n"
              f"Using Python, generate a visualization based on this prompt: {user_prompt}\n"
              f"Use Plotly or Matplotlib for the visualization."
          )

          # Query GenAI for Python code
          st.write("### Generated Code")
          generated_code = query_genai(full_prompt)
          st.code(generated_code, language="python")

          # Execute the generated code
          st.write("### Visualization Output")
          result = execute_code(generated_code, df)

          if isinstance(result, str) and result.startswith("Error"):
              st.error(result)
          elif result is not None:
              st.plotly_chart(result) if isinstance(result, px.Figure) else st.pyplot(result)
          else:
              st.error("No visualization was generated. Please refine your prompt.")

else:
  st.info("Please upload a CSV file to get started.")

# Footer
st.markdown("---")
st.markdown("**Powered by Streamlit & OpenAI GPT-4**")



