import streamlit as st
import pandas as pd
import plotly.express as px

# Function to parse user prompts and determine the type of visualization
def parse_prompt(prompt):
 """
 Parse the user's natural language prompt to identify the chart type.
 Returns a dictionary with 'chart_type'.
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
def create_visualization(df, chart_type, x_column, y_column, aggregation):
 # Apply aggregation if necessary
 if aggregation == "count":
     df = df.groupby(x_column).size().reset_index(name="count")
     y_column = "count"
 elif aggregation == "sum" and y_column in df.select_dtypes(include=["number"]).columns:
     df = df.groupby(x_column)[y_column].sum().reset_index()

 # Generate the appropriate chart
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
st.title("AI-Powered Dashboard (With Aggregation Options)")

# Step 1: File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
 # Load the dataset
 df = pd.read_csv(uploaded_file)
 st.write("### Dataset Preview")
 st.dataframe(df.head())

 # Initialize session state variables
 if "chart_type" not in st.session_state:
     st.session_state.chart_type = None
 if "x_column" not in st.session_state:
     st.session_state.x_column = None
 if "y_column" not in st.session_state:
     st.session_state.y_column = None
 if "aggregation" not in st.session_state:
     st.session_state.aggregation = "sum"

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
         st.session_state.chart_type = parsed_prompt["chart_type"]

         if st.session_state.chart_type is None:
             st.error("Sorry, I couldn't understand the type of visualization you want. Please refine your prompt.")
         else:
             st.success(f"Detected chart type: {st.session_state.chart_type.capitalize()} Chart")

 # If a chart type has been detected, allow column selection
 if st.session_state.chart_type:
     st.write("### Select Columns and Aggregation for Visualization")
     st.session_state.x_column = st.selectbox("Select X-axis column:", df.columns, key="x_column_select")
     st.session_state.y_column = st.selectbox("Select Y-axis column:", df.columns, key="y_column_select")

     # Show aggregation options only for numeric columns
     if st.session_state.y_column in df.select_dtypes(include=["number"]).columns:
         st.session_state.aggregation = st.selectbox(
             "Select Aggregation Method:",
             ["sum", "count"],
             key="aggregation_select"
         )
     else:
         st.session_state.aggregation = "count"  # Default to count for non-numeric columns

     # Generate and display the visualization
     if st.session_state.x_column and st.session_state.y_column:
         fig = create_visualization(
             df,
             st.session_state.chart_type,
             st.session_state.x_column,
             st.session_state.y_column,
             st.session_state.aggregation
         )
         if fig:
             st.plotly_chart(fig)
         else:
             st.error("An error occurred while generating the visualization.")

else:
 st.info("Please upload a CSV file to get started.")

# Footer
st.markdown("---")
st.markdown("**Powered by Streamlit & Plotly**")
