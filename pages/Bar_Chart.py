import streamlit as st
import pandas as pd
import plotly.express as px
import openai

# Set up OpenAI API Key
openai.api_key = st.secrets["openai_api_key"]

# Function to get AI-generated insights
def get_insights_from_ai(chart_data):
try:
    prompt = f"""
    You are a data analyst. Provide insights about the following bar chart data:
    {chart_data.to_string(index=False)}
    """
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

# Bar Chart Page
st.title("Bar Chart Visualization")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
df = pd.read_csv(uploaded_file)
st.write("### Dataset Preview")
st.dataframe(df.head())

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
    insights = get_insights_from_ai(chart_data)
    st.write(insights)
else:
st.info("Please upload a CSV file to get started.")
