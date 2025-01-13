from core.readers import FileReaderFactory
from core.preprocessing import DataPreprocessor
from core.plots import PlotContext
from core.dim_reduction import DimReductionFactory
from core.singleton import SingletonMeta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DataAnalysisFacade(metaclass=SingletonMeta):
    """
    Facade class that simplifies interaction with data reading, preprocessing, and visualization.
    """
    def __init__(self):
        logging.info("Initializing DataAnalysisFacade")
        self.data = None
        self.preprocessor = None
        self.plot_context = None


    def load_data(self, file):
        """
        Load data using the appropriate reader based on file extension.

        :param file_path: str - Path to the file to load.
        :return: pd.DataFrame - Loaded data.
        """
        reader = FileReaderFactory.get_reader(file)
        self.data = reader.read(file)
        self.preprocessor = DataPreprocessor(self.data)
        return self.data

    def preprocess_data(self, handle_nulls=None, rename_map=None, drop_cols=None):
        """
        Perform preprocessing steps like handling nulls, renaming, and dropping columns.

        :param handle_nulls: dict - Options for handling nulls (e.g., {"method": "mean"}).
        :param rename_map: dict - Column renaming map (e.g., {"old_name": "new_name"}).
        :param drop_cols: list - Columns to drop.
        :return: pd.DataFrame - Preprocessed data.
        """
        if handle_nulls:
            method = handle_nulls.get("method", "mean")
            fill_value = handle_nulls.get("fill_value", None)
            self.preprocessor.handle_nulls(method=method, fill_value=fill_value)

        if rename_map:
            self.preprocessor.rename_columns(rename_map)

        if drop_cols:
            self.preprocessor.drop_columns(drop_cols)
            
        return self.preprocessor.get_data() 

    def create_plot(self, plot_type, plot_subtype, **kwargs):
        """
        Create a plot using the provided plot type and parameters.

        :param plot_type: str - The type of plot (e.g., "line", "scatter").
        :param title: str - Title for the plot.
        :param kwargs: Additional parameters for the specific plot type.
        :return: Plotly Figure - The generated plot.
        """
        if self.plot_context is None:
            self.plot_context = PlotContext(None)
        
        if plot_type != 'dimensionality_reduction':
            self.plot_context.set_strategy(plot_type)
            self.plot_context.update_plot(self.preprocessor.get_data(), **kwargs)
        else:
            reduction_technique = DimReductionFactory.get_reducer(plot_subtype, **kwargs)

            fig=reduction_technique.create_plot()
            self.plot_context.set_plot(fig)
        return self.plot_context.fig
    