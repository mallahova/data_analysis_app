import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Title and description
st.title("Data Analysis and Visualization App Prototype")
st.markdown(
    """ 
    This app is a prototype for data analysis and visualization. 
    You can upload a dataset, perform optional preprocessing, and visualize the results.
    Note: Functionality is not implemented yet, this is a visual prototype.
    """
)

# File Upload
st.sidebar.header("Step 1: Upload Your Dataset")
data_file = st.sidebar.file_uploader("Upload CSV or JSON file", type=["csv", "json"])

# Initialize session state for keeping track of preprocessing steps
if 'preprocessing_done' not in st.session_state:
    st.session_state.preprocessing_done = False

if data_file:
    if data_file.name.endswith(".csv"):
        data = pd.read_csv(data_file)
    else:
        data = pd.read_json(data_file)

    st.write("### Preview of Uploaded Data")
    st.write(data.head())

    # Preprocessing Options (Step 2)
    st.sidebar.header("Step 2: Preprocessing Options")
    st.sidebar.markdown("Choose preprocessing steps")

    handle_nulls = st.sidebar.checkbox("Handle Null Values")
    if handle_nulls:
        st.sidebar.markdown("#### Handle Null Values")
        null_option = st.sidebar.radio(
            "Select a method to handle null values:",
            ("Use mean()", "Drop NA", "Insert 0 in place of null")
        )
        st.sidebar.markdown(f"Selected option: {null_option}")

    rename_columns = st.sidebar.checkbox("Rename Columns")
    if rename_columns:
        st.sidebar.markdown("#### Rename Columns")
        st.sidebar.markdown("(Dummy UI: Provide a mapping for renaming)")
        old_col = st.sidebar.selectbox("Select column to rename", data.columns)
        new_col = st.sidebar.text_input(f"Rename {old_col} to:")

    drop_columns = st.sidebar.checkbox("Drop Columns")
    if drop_columns:
        st.sidebar.markdown("#### Drop Columns")
        st.sidebar.markdown("(Dummy UI: Select columns to drop)")

    preprocess_button = st.sidebar.button("Preprocess")
    continue_without_preprocessing_button = st.sidebar.button("Continue Without Preprocessing")

    # Mark the preprocessing as done when one of the buttons is clicked
    if preprocess_button or continue_without_preprocessing_button:
        st.session_state.preprocessing_done = True

    # Visualization, Dashboard, and Additional Analysis appear only after clicking "Preprocess" or "Continue Without Preprocessing"
    if st.session_state.preprocessing_done:
        # Step 3: Visualization
        st.sidebar.header("Step 3: Visualization")
        st.sidebar.markdown("You can create multiple plots and add them to the dashboard.")

        plot_type = st.sidebar.selectbox(
            "Select a Plot Type", ["None", "Line Plot", "Scatter Plot", "Histogram", "Heatmap", "Boxplot"]
        )

        if plot_type != "None":
            st.sidebar.markdown(f"#### Create {plot_type}")
            x_column = st.sidebar.selectbox("Select X-axis column", data.columns, key=f"x_{plot_type}")
            y_column = st.sidebar.selectbox("Select Y-axis column", data.columns, key=f"y_{plot_type}")

            if plot_type == "Scatter Plot":
                marker_style = st.sidebar.radio("Select marker style", ["x", "o", ".", "+", "*"], key=f"marker_{plot_type}")
                st.sidebar.markdown(f"Selected marker style: {marker_style}")

            add_to_dashboard = st.sidebar.button(f"Add {plot_type} to Dashboard", key=f"add_{plot_type}")

            if add_to_dashboard:
                st.write(f"{plot_type} added to the dashboard (dummy action).")

            # Dummy Interactive Plots using Plotly
            st.write(f"### {plot_type} Visualization (Interactive Plot)")

            if plot_type == "Line Plot":
                # Interactive Line Plot
                x = np.linspace(0, 10, 100)
                y = np.sin(x)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name="sin(x)"))
                fig.update_layout(title="Line Plot: sin(x)", xaxis_title=x_column, yaxis_title=y_column)
                st.plotly_chart(fig)

            elif plot_type == "Scatter Plot":
                # Interactive Scatter Plot
                x = np.random.rand(50)
                y = np.random.rand(50)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(symbol=marker_style)))
                fig.update_layout(title="Scatter Plot: Random Data", xaxis_title=x_column, yaxis_title=y_column)
                st.plotly_chart(fig)

            elif plot_type == "Histogram":
                # Interactive Histogram
                data_values = np.random.randn(1000)
                fig = go.Figure()
                fig.add_trace(go.Histogram(x=data_values, nbinsx=30))
                fig.update_layout(title="Histogram: Random Data Distribution", xaxis_title=x_column, yaxis_title=y_column)
                st.plotly_chart(fig)

            elif plot_type == "Heatmap":
                # Dummy Heatmap
                corr_data = np.random.rand(10, 10)
                fig = go.Figure(data=go.Heatmap(z=corr_data, colorscale='Viridis'))
                fig.update_layout(title="Heatmap: Random Data Correlation")
                st.plotly_chart(fig)

            elif plot_type == "Boxplot":
                # Dummy Boxplot
                data_values = np.random.randn(100)
                fig = go.Figure()
                fig.add_trace(go.Box(y=data_values, boxmean='sd'))
                fig.update_layout(title="Boxplot: Random Data Distribution")
                st.plotly_chart(fig)

        # Step 4: Dashboard
        st.sidebar.header("Step 4: Dashboard")
        show_dashboard = st.sidebar.checkbox("Show Dashboard")

        if show_dashboard:
            st.write("## Dashboard")
            st.write("(Dummy UI: A collection of added plots and metrics)")


        # Step 6: Clustering (K-means)
        st.sidebar.header("Step 5:  Additional Analysis")
        show_clustering = st.sidebar.checkbox("Perform K-means Clustering")

        if show_clustering:
            st.write("## K-means Clustering")
            # Dummy clustering (using random data)
            X = np.random.rand(100, 2)  # Random 2D data
            kmeans = KMeans(n_clusters=3)
            kmeans.fit(X)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode='markers', marker=dict(color=kmeans.labels_)))
            fig.update_layout(title="K-means Clustering", xaxis_title="Feature 1", yaxis_title="Feature 2")
            st.plotly_chart(fig)

        # Step 7: Downloadable Reports
        st.sidebar.header("Step 7: Downloadable Reports")
        download_data = st.sidebar.button("Download Cleaned Data")
        download_plot = st.sidebar.button("Download Plot as PNG")

        if download_data:
            st.write("Download cleaned data (dummy functionality).")
        
        if download_plot:
            st.write("Download plot as PNG (dummy functionality).")

else:
    st.write("Please upload a dataset to proceed.")
