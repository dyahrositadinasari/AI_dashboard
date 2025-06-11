import streamlit as st
import pandas as pd
import plotly.express as px
import openai  # For AI-generated insights

# Set up OpenAI API Key
openai.api_key = st.secrets["openai_api_key"]

# Function to get AI-generated insights
def get_insights_from_ai(chart_data, chart_type):
 """
 Send the chart data and type to OpenAI to generate insights.
 """
 try:
     # Prepare the prompt
     prompt = f"""
     You are a data analyst. Provide insights about the following {chart_type} visualization:
     {chart_data.to_string(index=False)}
     """

     # Query OpenAI
     response = openai.ChatCompletion.create(
         model="gpt-3.5-turbo",
         messages=[
             {"role": "system", "content": "You are a helpful assistant that provides insights about data visualizations."},
             {"role": "user", "content": prompt}
         ],
         temperature=0.7,
     )
     return response['choices'][0]['message']['content']
 except Exception as e:
     return f"Error generating insights: {e}"

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Bar Chart", "Line Chart", "Scatter Plot"])

# File Upload (shared across all pages)
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
 df = pd.read_csv(uploaded_file)

 # Home Page
 if page == "Home":
     st.title("Welcome to the Visualization Dashboard!")
     st.write("""
     This app allows you to create custom visualizations and get AI-powered insights for your data.
     
     Use the sidebar to navigate to different visualization types:
     - **Bar Chart**
     - **Line Chart**
     - **Scatter Plot**
     """)
     st.write("### Dataset Preview")
     st.dataframe(df.head())

 # Bar Chart Page
 elif page == "Bar Chart":
     st.title("Bar Chart Visualization")
     st.write("Create a bar chart by selecting columns and aggregation method.")

     x_column = st.selectbox("Select X-axis column:", df.columns)
     y_column = st.selectbox("Select Y-axis column:", df.columns)
     aggregation = st.selectbox("Select aggregation method for Y-axis:", ["sum", "count", "average"])

     if st.button("Generate Bar Chart"):
         # Apply aggregation
         if aggregation == "sum":
             chart_data = df.groupby(x_column)[y_column].sum().reset_index()
         elif aggregation == "count":
             chart_data = df.groupby(x_column).size().reset_index(name="count")
             y_column = "count"
         elif aggregation == "average":
             chart_data = df.groupby(x_column)[y_column].mean().reset_index()

         # Create bar chart
         fig = px.bar(chart_data, x=x_column, y=y_column, title=f"Bar Chart of {y_column} by {x_column}")
         st.plotly_chart(fig)

         # Generate AI Insights
         st.write("### AI-Generated Insights")
         insights = get_insights_from_ai(chart_data, "Bar Chart")
         st.write(insights)

 # Line Chart Page
 elif page == "Line Chart":
     st.title("Line Chart Visualization")
     st.write("Create a line chart by selecting columns.")

     x_column = st.selectbox("Select X-axis column:", df.columns)
     y_column = st.selectbox("Select Y-axis column:", df.columns)

     if st.button("Generate Line Chart"):
         # Create line chart
         fig = px.line(df, x=x_column, y=y_column, title=f"Line Chart of {y_column} vs {x_column}")
         st.plotly_chart(fig)

         # Generate AI Insights
         st.write("### AI-Generated Insights")
         insights = get_insights_from_ai(df[[x_column, y_column]], "Line Chart")
         st.write(insights)

 # Scatter Plot Page
 elif page == "Scatter Plot":
     st.title("Scatter Plot Visualization")
     st.write("Create a scatter plot by selecting columns.")

     x_column = st.selectbox("Select X-axis column:", df.columns)
     y_column = st.selectbox("Select Y-axis column:", df.columns)

     if st.button("Generate Scatter Plot"):
         # Create scatter plot
         fig = px.scatter(df, x=x_column, y=y_column, title=f"Scatter Plot of {y_column} vs {x_column}")
         st.plotly_chart(fig)

         # Generate AI Insights
         st.write("### AI-Generated Insights")
         insights = get_insights_from_ai(df[[x_column, y_column]], "Scatter Plot")
         st.write(insights)

else:
 st.title("Welcome to the Visualization Dashboard!")
 st.write("Please upload a CSV file to get started.")
