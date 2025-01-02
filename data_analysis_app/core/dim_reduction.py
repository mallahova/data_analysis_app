from abc import ABC, abstractmethod
from sklearn.decomposition import PCA
from umap import UMAP
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from core.plots import PlotContext, ScatterPlotStrategy,PlotStrategy
from plotly.graph_objects import Figure

class DimReduction(ABC):
    """
    Abstract Base Class for Dimensionality Reduction.
    Implements the Template Method Design Pattern.
    """

    def __init__(self, data: pd.DataFrame, columns: list = None, n_components: int = 2, categorical_column=None, title=""):
        """
        Initialize the dimensionality reduction algorithm.

        :param data: The dataset (Pandas DataFrame).
        :param columns: The list of columns to use for dimensionality reduction. If None, use all columns.
        :param n_components: Number of components/dimensions to reduce to.
        """
        self.data = data
        self.columns = columns or data.columns  # Use all columns if none are specified
        self.n_components = n_components
        self.categorical_column=categorical_column
        self.title=title
        

        # Validate that selected columns exist in the data
        for col in self.columns:
            if col not in data.columns:
                raise ValueError(f"Column '{col}' not found in the dataset.")

        # Subset the data
        self.data = data[self.columns]

        # Scaled data is initialized but not scaled until preprocessing
        self.scaled_data = None

    def preprocess_data(self):
        """
        Preprocess the data (e.g., standardize features). This is the same for all subclasses.
        """
        categorical_columns = self.data.select_dtypes(include=['object']).columns
        self.scaled_data = pd.get_dummies(self.data, columns=categorical_columns)
        scaler = StandardScaler()
        self.scaled_data = scaler.fit_transform(self.scaled_data)

    @abstractmethod
    def apply_reduction(self):
        """
        Perform the specific dimensionality reduction technique.
        Must be implemented by subclasses.
        """
        pass

    def postprocess_results(self, reduced_data: np.ndarray) -> pd.DataFrame:
        """
        Post-process the results (convert to a DataFrame and return).
        """
        columns = [f"Component_{i+1}" for i in range(self.n_components)]
        return pd.DataFrame(reduced_data, columns=columns)

    def run(self):
        """
        The Template Method that defines the overall process for dimensionality reduction.
        """
        print("(Dim Reduction) Preprocessing data...")
        self.preprocess_data()

        print("Applying dimensionality reduction...")
        reduced_data = self.apply_reduction()

        print("Postprocessing results...")
        return self.postprocess_results(reduced_data)

    def create_plot(self):
        red_result = self.run()
        if self.categorical_column:
            red_result[self.categorical_column] = self.data[self.categorical_column]
        scatter_strategy=ScatterPlotStrategy()
        fig=scatter_strategy.create_plot(
            fig=Figure(),
            data=red_result,
            title=self.title,
            x_column="Component_1",
            y_column="Component_2",
            categorical_column=self.categorical_column
        )
        return fig

class PCAAnalysis(DimReduction):
    """
    Concrete implementation of Dimensionality Reduction using PCA.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def apply_reduction(self):
        """
        Perform PCA on the preprocessed data.
        """
        pca = PCA(n_components=self.n_components)
        return pca.fit_transform(self.scaled_data)


class UMAPAnalysis(DimReduction):
    """
    Concrete implementation of Dimensionality Reduction using UMAP.
    """

    def __init__(self, n_neighbors: int = 15, min_dist: float = 0.1,**kwargs):
        """
        Initialize UMAP-specific parameters.

        :param n_neighbors: Number of neighbors for UMAP.
        :param min_dist: Minimum distance between points for UMAP.
        """
        super().__init__(**kwargs)
        self.n_neighbors = n_neighbors
        self.min_dist = min_dist

    def apply_reduction(self):
        """
        Perform UMAP on the preprocessed data.
        """
        umap = UMAP(n_components=self.n_components, n_neighbors=self.n_neighbors, min_dist=self.min_dist,metric="euclidean")
        return umap.fit_transform(self.scaled_data)

class DimReductionFactory:
    @staticmethod
    def get_reducer(dim_reduction_type: str, **kwargs):
        if dim_reduction_type == "PCA":
            return PCAAnalysis(**kwargs)
        elif dim_reduction_type == "UMAP":
            return UMAPAnalysis(**kwargs)
        else:
            raise ValueError(f"Unknown dimensionality reduction type: {dim_reduction_type}")