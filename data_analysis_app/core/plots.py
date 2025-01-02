"""
This module implements dynamically updating plot based on user input. A strategy design pattern is used to implement specific plot types.
"""
from abc import ABC, abstractmethod
from plotly.graph_objects import Figure, Scatter, Histogram, Heatmap, Box
from plotly.graph_objs import Scattergl
import plotly.io as pio
import plotly.express as px




class PlotStrategy(ABC):
    @abstractmethod
    def create_plot(self,fig, data, title: str, **kwargs) -> Figure:
        """Creates a plot based on the provided data and parameters."""
        pass


class LinePlotStrategy(PlotStrategy):
    def create_plot(self, fig, data, title: str, x_column, y_column, line_color="blue", line_width=2):
        fig.add_trace(Scatter(x=data[x_column], y=data[y_column], mode="lines",
                              line=dict(color=line_color, width=line_width)))
        fig.update_layout(title=title, xaxis_title=x_column, yaxis_title=y_column)
        return fig


# class ScatterPlotStrategy(PlotStrategy):
#     def create_plot(self, fig, data, title: str, x_column, y_column, marker_symbol="circle", marker_color="red"):
#         fig.add_trace(Scattergl(x=data[x_column], y=data[y_column], mode="markers",
#                                 marker=dict(symbol=marker_symbol, color=marker_color)))
#         fig.update_layout(title=title, xaxis_title=x_column, yaxis_title=y_column)
#         return fig

class ScatterPlotStrategy(PlotStrategy):
    def create_plot(self, fig, data, title: str, x_column, y_column, categorical_column=None, marker_symbol="circle"):
        """
        Creates a scatter plot, optionally using a categorical column to color the points.

        :param fig: The plotly figure.
        :param data: The dataframe containing the data.
        :param title: The plot title.
        :param x_column: The column name for the x-axis.
        :param y_column: The column name for the y-axis.
        :param categorical_column: The categorical column name for coloring. Defaults to None.
        :param marker_symbol: The marker symbol. Defaults to "circle".
        :return: The updated plotly figure.
        """
        if categorical_column:
            color_map = px.colors.qualitative.Set1

            categories = data[categorical_column].unique()
            if len(categories) > len(color_map):
                raise ValueError(f"Not enough colors in the selected color scale for {len(categories)} categories.")

            for idx, category in enumerate(categories):
                category_data = data[data[categorical_column] == category]
                fig.add_trace(Scattergl(
                    x=category_data[x_column], 
                    y=category_data[y_column], 
                    mode="markers",
                    marker=dict(symbol=marker_symbol, color=color_map[idx]),
                    name=str(category)
                ))
        else:
            fig.add_trace(Scattergl(
                x=data[x_column], 
                y=data[y_column], 
                mode="markers", 
                marker=dict(symbol=marker_symbol, color="red")
            ))

        fig.update_layout(
            title=title,
            xaxis_title=x_column,
            yaxis_title=y_column
        )
        return fig


class HistogramStrategy(PlotStrategy):
    def create_plot(self, fig, data, title: str, x_column, bins=30, bar_color="green"):
        fig.add_trace(Histogram(x=data[x_column], nbinsx=bins, marker=dict(color=bar_color)))
        fig.update_layout(title=title, xaxis_title=x_column)
        return fig


class HeatmapStrategy(PlotStrategy):
    def create_plot(self, fig, data, title: str, x_column=None, y_column=None, z_column=None, colorscale="Viridis", max_points=30):
        if not (x_column and y_column and z_column):
            raise ValueError("Heatmap requires x_column, y_column, and z_column to be specified.")
        for col in [x_column, y_column]:
            if data[col].nunique() > 30:
                return fig
        fig.add_trace(Heatmap(
            x=data[x_column],
            y=data[y_column],
            z=data[z_column],
            colorscale=colorscale
        ))
        fig.update_layout(
            title=title,
            xaxis_title=x_column,
            yaxis_title=y_column
        )
        return fig



class BoxPlotStrategy(PlotStrategy):
    def create_plot(self, fig, data, title: str, x_column, box_color="orange"):
        fig.add_trace(Box(y=data[x_column], marker=dict(color=box_color), boxmean="sd"))
        fig.update_layout(title=title, yaxis_title=x_column)
        return fig


class PlotContext:
    def __init__(self, strategy: PlotStrategy):
        print("Initializing PlotContext...")
        self.strategy = strategy
        
    def _get_strategy(self, strategy_name: str):
        if strategy_name == "line":
            return LinePlotStrategy()
        elif strategy_name == "scatter":
            return ScatterPlotStrategy()
        elif strategy_name == "histogram":
            return HistogramStrategy()
        elif strategy_name == "heatmap":
            return HeatmapStrategy()
        elif strategy_name == "boxplot":
            return BoxPlotStrategy()
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

    def set_strategy(self, strategy_name: str):
        self.strategy = self._get_strategy(strategy_name)

    def update_plot(self, data, title: str, **kwargs):
        self.fig = Figure()
        self.fig= self.strategy.create_plot(self.fig, data, title, **kwargs)


#example code

# import pandas as pd
# import numpy as np
# from plotly.graph_objects import Figure

# # Example data
# data = pd.DataFrame({
#     "x": np.linspace(0, 10, 100),                  # 100 evenly spaced values between 0 and 10
#     "y": np.sin(np.linspace(0, 10, 100)),
#     "z": np.cos(np.linspace(0, 10, 100)),         # Sine function for y values
#                       # Sine function for y values
#     "category": np.random.choice(["A", "B", "C"], size=100),  # Random categorical values
# })

# # Initialize PlotContext with a LinePlotStrategy
# plot_context = PlotContext(LinePlotStrategy())

# # Test Line Plot
# plot_context.set_strategy("line")
# plot_context.update_plot(data, title="Line Plot Example", x_column="x", y_column="y", line_color="blue", line_width=3)
# plot_context.fig.show()

# # Test Scatter Plot
# plot_context.set_strategy("scatter")
# plot_context.update_plot(data, title="Scatter Plot Example", x_column="x", y_column="y", marker_symbol="circle", marker_color="green")
# plot_context.fig.show()

# # Test Histogram
# plot_context.set_strategy("histogram")
# plot_context.update_plot(data, title="Histogram Example", x_column="x", bins=20, bar_color="purple")
# plot_context.fig.show()

# # Test Heatmap
# plot_context.set_strategy("heatmap")
# plot_context.update_plot(data, title="Heatmap Example", z_data=data["z"].values, colorscale="Viridis")
# plot_context.fig.show()

# # Test Box Plot
# plot_context.set_strategy("boxplot")
# plot_context.update_plot(data, title="Box Plot Example", y_column="y", box_color="orange")
# plot_context.fig.show()
