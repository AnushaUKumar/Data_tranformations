import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

# Dashboard colors
colors = {
    "sky_blue": "#C1E8F8",
    "cool_cyan": "#60D1F2",
    "indigo_blue": "#6074F2",
    "soft_purple": "#B8A7F8",
    "soft_green": "#CFF5D3",
    "bold_green": "#4BB543"
}

# Page config
st.set_page_config(page_title="Scaling Dashboard", layout="wide")

# --- Layout ---
col1, col2 = st.columns([1, 3])  # Sidebar-like ratio

with col1:
    st.markdown("### Controls")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        if not numeric_cols:
            st.warning("No numeric columns found.")
        else:
            selected_col = st.selectbox("Choose column", numeric_cols)
            method = st.radio("Scaling Method", ["Min-Max", "Z-score", "Robust"])
            view = st.radio("Comparison Type", ["Line Plot", "Histogram"])
    else:
        st.info("Upload a CSV with numeric data.")

# Only show charts if file is uploaded
if uploaded_file and selected_col:

    # Extract data
    original_data = df[[selected_col]].dropna()

    if method == "Min-Max":
        scaler = MinMaxScaler()
        label = "Min-Max Scaled"
        color = colors["cool_cyan"]
        fill = colors["sky_blue"]
    elif method == "Z-score":
        scaler = StandardScaler()
        label = "Z-score Scaled"
        color = colors["indigo_blue"]
        fill = colors["soft_purple"]
    else:
        scaler = RobustScaler()
        label = "Robust Scaled"
        color = colors["bold_green"]
        fill = colors["soft_green"]

    scaled_data = scaler.fit_transform(original_data)
    preview_len = min(100, len(original_data))

    plot_df = pd.DataFrame({
        "Original": original_data.iloc[:preview_len, 0].values,
        "Scaled": scaled_data[:preview_len, 0]
    })

    # --- MAIN CONTENT ---
    with col2:
        st.markdown(f"###  Data Transformation: Original vs {label}")

        if view == "Line Plot":
            fig, axs = plt.subplots(1, 2, figsize=(14, 5))

            axs[0].plot(plot_df["Original"], color=colors["indigo_blue"], marker='o')
            axs[0].fill_between(range(preview_len), plot_df["Original"], color=fill, alpha=0.3)
            axs[0].set_title("Original Data", color=colors["indigo_blue"])
            axs[0].grid(True, color=colors["sky_blue"], linestyle='--', alpha=0.3)

            axs[1].plot(plot_df["Scaled"], color=color, marker='s')
            axs[1].fill_between(range(preview_len), plot_df["Scaled"], color=fill, alpha=0.3)
            axs[1].set_title(f"{label}", color=color)
            axs[1].grid(True, color=colors["sky_blue"], linestyle='--', alpha=0.3)

            st.pyplot(fig)

        elif view == "Histogram":
            fig, axs = plt.subplots(1, 2, figsize=(14, 4))

            axs[0].hist(plot_df["Original"], bins=30, color=colors["indigo_blue"], edgecolor='white', alpha=0.8)
            axs[0].set_title("Original Distribution", color=colors["indigo_blue"])

            axs[1].hist(plot_df["Scaled"], bins=30, color=color, edgecolor='white', alpha=0.8)
            axs[1].set_title(f"{label} Distribution", color=color)

            st.pyplot(fig)

        # Explanation Box
        st.markdown(f"""
        <div style="background-color:{colors['soft_green']};padding:15px;border-radius:8px;margin-top:20px;">
            <h4 style="color:{colors['bold_green']};margin-bottom:0;">Scaling Method: {label}</h4>
            <p style="color:#333;margin-top:5px;">
                This method transforms the selected column to a new scale.<br>
                Compare both charts to see how the data's <b>center, spread, and range</b> have changed.
            </p>
        </div>
        """, unsafe_allow_html=True)
