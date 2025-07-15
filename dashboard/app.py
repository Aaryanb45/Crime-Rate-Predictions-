import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from st_aggrid import AgGrid, GridOptionsBuilder
import os

# Updated paths for Docker container
st.write("📂 Working Directory:", os.getcwd())
st.write("📄 Files in /app/data:", os.listdir("/app/data"))

st.set_page_config(page_title="Crime Rate Dashboard", layout="wide")
st.title("🚨 Crime Rate Prediction Dashboard")

# ✅ Load and preprocess data
df = pd.read_csv("/app/data/cleaned_crime_data.csv", engine='python')
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

model = KMeans(n_clusters=4, random_state=42)
df['CLUSTER'] = model.fit_predict(scaled_data)
df['TOTAL_CRIMES'] = df.sum(axis=1)

cluster_labels = {
    0: "Low Risk",
    1: "Moderate Risk",
    2: "High Risk",
    3: "Severe Risk"
}
df['LABEL'] = df['CLUSTER'].map(cluster_labels)

# Sidebar filters
st.sidebar.header("🔎 Filter Clusters")
selected_clusters = st.sidebar.multiselect("Select Cluster Labels:", options=list(cluster_labels.values()), default=list(cluster_labels.values()))
filtered_df = df[df['LABEL'].isin(selected_clusters)]

# Plotly pie chart for cluster distribution
st.subheader("📊 Cluster Distribution")
fig_pie = px.pie(filtered_df, names='LABEL', title='Crime Risk Distribution by Cluster')
st.plotly_chart(fig_pie, use_container_width=True)

# Bar chart for total crimes per cluster
st.subheader("📈 Crimes per Cluster")
fig_bar = px.bar(
    filtered_df.groupby('LABEL')['TOTAL_CRIMES'].sum().reset_index(),
    x='LABEL', y='TOTAL_CRIMES',
    color='LABEL',
    text_auto=True,
    title="Total Crimes per Risk Category"
)
st.plotly_chart(fig_bar, use_container_width=True)

# AgGrid summary table
st.subheader("📋 Interactive Crime Table")
gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination()
gb.configure_side_bar()
gb.configure_default_column(editable=False, groupable=True)
AgGrid(filtered_df, gridOptions=gb.build(), enable_enterprise_modules=True, theme='balham')

# Upload section
st.subheader("📁 Upload Your Own CSV to Predict Cluster")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        user_df = pd.read_csv(uploaded_file)

        # Ensure only numeric columns
        numeric_user_df = user_df.select_dtypes(include=np.number)

        # Check dimension match
        if numeric_user_df.shape[1] != scaled_data.shape[1]:
            st.warning(f"⚠️ Uploaded data has {numeric_user_df.shape[1]} numeric features but model expects {scaled_data.shape[1]}. Results may be inaccurate.")

        # Trim or pad columns
        min_cols = min(numeric_user_df.shape[1], scaled_data.shape[1])
        input_to_model = numeric_user_df.iloc[:, :min_cols]

        if min_cols < scaled_data.shape[1]:
            padding = np.zeros((input_to_model.shape[0], scaled_data.shape[1] - min_cols))
            input_to_model = np.hstack([input_to_model.values, padding])

        # Convert to DataFrame for easier NaN handling
        input_to_model = pd.DataFrame(input_to_model)

        # Fill missing values with column means
        input_to_model.fillna(input_to_model.mean(), inplace=True)

        # Scale and predict
        user_scaled = scaler.transform(input_to_model)
        user_clusters = model.predict(user_scaled)

        user_df['CLUSTER'] = user_clusters
        user_df['LABEL'] = user_df['CLUSTER'].map(cluster_labels)

        st.success("✅ Predictions complete!")
        st.dataframe(user_df)

    except Exception as e:
        st.error(f"⚠️ Error processing uploaded file: {e}")
