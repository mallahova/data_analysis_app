from abc import ABC, abstractmethod
from sklearn.decomposition import PCA
from umap import UMAP
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

class DimensionalityReduction(ABC):
    """
    Abstract Base Class for Dimensionality Reduction.
    Implements the Template Method Design Pattern.
    """

    def __init__(self, data: pd.DataFrame, columns: list = None, n_components: int = 2):
        """
        Initialize the dimensionality reduction algorithm.

        :param data: The dataset (Pandas DataFrame).
        :param columns: The list of columns to use for dimensionality reduction. If None, use all columns.
        :param n_components: Number of components/dimensions to reduce to.
        """
        self.data = data
        self.columns = columns or data.columns  # Use all columns if none are specified
        self.n_components = n_components

        # Validate that selected columns exist in the data
        for col in self.columns:
            if col not in data.columns:
                raise ValueError(f"Column '{col}' not found in the dataset.")

        # Subset the data
        self.selected_data = data[self.columns]

        # Scaled data is initialized but not scaled until preprocessing
        self.scaled_data = None

    def preprocess_data(self):
        """
        Preprocess the data (e.g., standardize features). This is the same for all subclasses.
        """
        scaler = StandardScaler()
        self.scaled_data = scaler.fit_transform(self.selected_data)

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
        print("Preprocessing data...")
        self.preprocess_data()

        print("Applying dimensionality reduction...")
        reduced_data = self.apply_reduction()

        print("Postprocessing results...")
        return self.postprocess_results(reduced_data)


class PCAAnalysis(DimensionalityReduction):
    """
    Concrete implementation of Dimensionality Reduction using PCA.
    """

    def __init__(self, data: pd.DataFrame, columns: list = None, n_components: int = 2):
        super().__init__(data, columns, n_components)

    def apply_reduction(self):
        """
        Perform PCA on the preprocessed data.
        """
        pca = PCA(n_components=self.n_components)
        return pca.fit_transform(self.scaled_data)


class UMAPAnalysis(DimensionalityReduction):
    """
    Concrete implementation of Dimensionality Reduction using UMAP.
    """

    def __init__(self, data: pd.DataFrame, columns: list = None, n_components: int = 2, n_neighbors: int = 15, min_dist: float = 0.1):
        """
        Initialize UMAP-specific parameters.

        :param n_neighbors: Number of neighbors for UMAP.
        :param min_dist: Minimum distance between points for UMAP.
        """
        super().__init__(data, columns, n_components)
        self.n_neighbors = n_neighbors
        self.min_dist = min_dist

    def apply_reduction(self):
        """
        Perform UMAP on the preprocessed data.
        """
        umap = UMAP(n_components=self.n_components, n_neighbors=self.n_neighbors, min_dist=self.min_dist)
        return umap.fit_transform(self.scaled_data)


# Example Usage
if __name__ == "__main__":
    # Example dataset
    data = pd.DataFrame({
        "Feature1": np.random.rand(100),
        "Feature2": np.random.rand(100),
        "Feature3": np.random.rand(100),
        "Feature4": np.random.rand(100),
    })

    # PCA Example
    print("\n--- PCA Example ---")
    pca_analysis = PCAAnalysis(data, columns=["Feature1", "Feature2", "Feature3"], n_components=2)
    pca_result = pca_analysis.run()
    print(pca_result.head())

    # UMAP Example
    print("\n--- UMAP Example ---")
    umap_analysis = UMAPAnalysis(data, columns=["Feature1", "Feature2", "Feature3"], n_components=2, n_neighbors=10, min_dist=0.2)
    umap_result = umap_analysis.run()
    print(umap_result.head())
