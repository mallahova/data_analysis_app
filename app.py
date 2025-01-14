import streamlit as st
from core.facade import DataAnalysisFacade
import plotly.graph_objects as go

st.set_page_config(
    page_title="Visualize, visualize, visualize!",
    page_icon="assets/visualization-eye-svgrepo-com.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)

col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("assets/visualization-eye-svgrepo-com.svg", width=40)
with col1:
    st.title("Visualize, visualize, visualize!")
st.markdown(
    "This app allows you to upload datasets, preprocess them, and visualize the results interactively."
)

if "current_page" not in st.session_state:
    st.session_state.current_page = "preprocessing"
if "data_file" not in st.session_state:
    st.session_state.data_file = None
if "preprocessing_done" not in st.session_state:
    st.session_state.preprocessing_done = False
if "preprocessed_data" not in st.session_state:
    st.session_state.preprocessed_data = None
if "facade" not in st.session_state:
    st.session_state.facade = DataAnalysisFacade()  # Initialize the facade once

facade = st.session_state.facade  # Access the single instance

# Sidebar - Step 1: Upload Dataset
if st.session_state.current_page == "preprocessing":
    st.sidebar.header("Step 1: Upload Dataset")
    data_file = st.sidebar.file_uploader(
        "Upload CSV or JSON file", type=["csv", "json"]
    )
    use_example = st.sidebar.button("Use an example dataset")
    if use_example:
        st.session_state.data_file = "samples/diamonds.csv"
    if data_file:
        st.session_state.data_file = data_file

# Load data if available
if st.session_state.data_file:
    # Initialize DataPreprocessor and PlotContext only once
    if "preprocessor" not in st.session_state:
        data = facade.load_data(st.session_state.data_file)
        st.session_state.preprocessor = facade.preprocessor  # Store the preprocessor
        st.session_state.plot_context = facade.plot_context  # Store the plot context
    else:
        data = (
            st.session_state.preprocessor.get_data()
        )  # Use the preprocessed data from session state

    preview_data = data.iloc[:100, :100]

    # Preprocessing page
    if st.session_state.current_page == "preprocessing":
        st.subheader("Preview of Uploaded Data")
        st.dataframe(preview_data)

        # Sidebar - Step 2: Preprocessing
        st.sidebar.header("Step 2: Preprocessing")
        handle_nulls = st.sidebar.checkbox("Handle Null Values")
        rename_columns = st.sidebar.checkbox("Rename Columns")
        drop_columns = st.sidebar.checkbox("Drop Columns")

        preprocessing_options = {}
        if handle_nulls:
            method = st.sidebar.radio(
                "Select method to handle nulls:", ("mean", "drop", "fill_with_0")
            )
            preprocessing_options["handle_nulls"] = {"method": method}
        if rename_columns:
            rename_map = {}
            old_col = st.sidebar.selectbox(
                "Select column to rename", facade.data.columns
            )
            new_col = st.sidebar.text_input("Rename column to:")
            if old_col and new_col:
                rename_map[old_col] = new_col
            preprocessing_options["rename_map"] = rename_map
        if drop_columns:
            cols_to_drop = st.sidebar.multiselect(
                "Select columns to drop", facade.data.columns
            )
            preprocessing_options["drop_cols"] = cols_to_drop

        preprocess_button = st.sidebar.button("Apply Preprocessing")
        continue_without_preprocessing_button = st.sidebar.button(
            "Continue Without Preprocessing"
        )
        if preprocess_button:
            st.session_state.preprocessed_data = facade.preprocess_data(
                **preprocessing_options
            )
            st.session_state.preprocessing_done = True
        if continue_without_preprocessing_button:
            st.session_state.preprocessing_done = True

        # Display preprocessed data
        if st.session_state.preprocessed_data is not None:
            st.write("### Preprocessed Data")
            st.dataframe(st.session_state.preprocessed_data.iloc[:100, :100])

        # Navigation for preprocessing
        if st.session_state.preprocessing_done:
            col1, col2 = st.columns([1, 1])
            with col2:
                go_to_visualization = st.button("Go to Visualization", key="go_button")
                if go_to_visualization:
                    st.session_state.current_page = "visualization"
                    st.rerun()

    elif st.session_state.current_page == "visualization":
        # Navigation for visualization
        col1, col2 = st.columns([1, 1])
        with col1:
            go_back = st.button("Go Back to Preprocessing", key="back_button")
            if go_back:
                st.session_state.current_page = "preprocessing"
                st.rerun()

        # Visualization page content
        st.sidebar.header("Step 3: Visualization")
        plot_type = st.sidebar.selectbox(
            "Select Plot Type",
            [
                "scatter",
                "line",
                "histogram",
                "boxplot",
                "heatmap",
                "dimensionality_reduction",
            ],
        )
        plot_subtype = None
        additional_params = {}

        if plot_type:
            if plot_type != "heatmap" and plot_type != "dimensionality_reduction":
                x_column = st.sidebar.selectbox(
                    "Select X-axis column",
                    st.session_state.preprocessor.get_data().columns,
                    key="x_column",
                )
                additional_params["x_column"] = x_column
                if plot_type in ["line", "scatter"]:
                    y_column = st.sidebar.selectbox(
                        "Select Y-axis column",
                        st.session_state.preprocessor.get_data().columns,
                        key="y_column",
                    )
                    additional_params["y_column"] = y_column

                    if plot_type == "line":
                        additional_params["line_color"] = st.sidebar.color_picker(
                            "Line Color", "#0000FF"
                        )
                        additional_params["line_width"] = st.sidebar.slider(
                            "Line Width", 1, 10, 2
                        )

                    if plot_type == "scatter":
                        # Add a selectbox for choosing a categorical column
                        categorical_column = st.sidebar.selectbox(
                            "Select Categorical Column for Coloring",
                            [None]
                            + list(
                                st.session_state.preprocessor.get_data()
                                .select_dtypes(include=["object"])
                                .columns
                            ),
                            key="categorical_column",
                        )
                        additional_params["categorical_column"] = categorical_column

                elif plot_type == "histogram":
                    additional_params["bins"] = st.sidebar.slider(
                        "Number of Bins", 5, 100, 30
                    )
                    additional_params["bar_color"] = st.sidebar.color_picker(
                        "Bar Color", "#00FF00"
                    )

                elif plot_type == "boxplot":
                    y_column = st.sidebar.selectbox(
                        "Select Y-axis column",
                        st.session_state.preprocessor.get_data().columns,
                        key="y_column",
                    )
                    additional_params["box_color"] = st.sidebar.color_picker(
                        "Box Color", "#FFA500"
                    )
            elif plot_type == "heatmap":
                x_column = st.sidebar.selectbox(
                    "Select X-axis column",
                    st.session_state.preprocessor.get_data()
                    .select_dtypes(include=["object"])
                    .columns,
                    key="x_column",
                )
                additional_params["x_column"] = x_column
                y_column = st.sidebar.selectbox(
                    "Select Y-axis column",
                    st.session_state.preprocessor.get_data()
                    .select_dtypes(include=["object"])
                    .columns,
                    key="y_column",
                )
                additional_params["y_column"] = y_column
                z_column = st.sidebar.selectbox(
                    "Select Z-axis column",
                    st.session_state.preprocessor.get_data().columns,
                    key="z_column",
                )
                additional_params["z_column"] = z_column
                additional_params["colorscale"] = st.sidebar.selectbox(
                    "Colorscale", ["Viridis", "Cividis", "Plasma"]
                )

            elif plot_type == "dimensionality_reduction":
                additional_params["data"] = st.session_state.preprocessor.get_data()
                reduction_method = st.sidebar.selectbox(
                    "Select Dimensionality Reduction Method", ["PCA", "UMAP"]
                )
                plot_subtype = reduction_method
                categorical_column = st.sidebar.selectbox(
                    "Select Categorical Column for Coloring",
                    [None]
                    + list(
                        st.session_state.preprocessor.get_data()
                        .select_dtypes(include=["object"])
                        .columns
                    ),
                    key="categorical_column",
                )
                additional_params["categorical_column"] = categorical_column

                if reduction_method == "UMAP":
                    n_neighbors = st.sidebar.slider("Select n_neighbors", 5, 50, 5)
                    min_dist = st.sidebar.slider("Select min_dist", 0.0, 1.0, 0.1)

                    # Default title and custom title input
            default_title = f"{plot_type.capitalize()} Plot"
            if plot_type in ["line", "scatter", "heatmap"]:
                default_title += f" X {x_column}, Y {y_column}"
                if plot_type == "heatmap":
                    default_title += f", Z {z_column}"
            elif plot_type in ["histogram"]:
                default_title += f" X {x_column}"
            elif plot_type == "boxplot":
                default_title += f" Y {y_column}"
            elif plot_type == "dimensionality_reduction":
                default_title = f"{reduction_method}"
            if additional_params.get("categorical_column", None):
                default_title += f" by {categorical_column}"

            custom_title = st.sidebar.text_input("Plot Title", default_title)
            additional_params["title"] = custom_title

            try:
                fig = st.session_state.facade.create_plot(
                    plot_type=plot_type, plot_subtype=plot_subtype, **additional_params
                )
                st.plotly_chart(fig)

                st.sidebar.header("Download Plot")

                def save_plot(fig, format):
                    img_bytes = fig.to_image(format=format)
                    return img_bytes

                file_format = st.sidebar.selectbox(
                    "Choose file format", ["png", "jpeg", "svg"]
                )

                img_bytes = save_plot(fig, file_format)

                mime_type = f"image/{file_format}"
                fig_title = fig.layout.title

                st.sidebar.download_button(
                    label=f"Download Plot as {file_format.upper()}",
                    data=img_bytes,
                    file_name=f"{fig_title['text'].replace(' ', '_')}.{file_format}",
                    mime=mime_type,
                )

            except Exception as e:
                st.error(f"Error creating plot: {e}")
