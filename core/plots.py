"""
This module implements dynamically updating plot based on user input. A strategy design pattern is used to implement specific plot types.
"""
from abc import ABC, abstractmethod
from plotly.graph_objects import Figure, Scatter, Histogram, Heatmap, Box
from plotly.graph_objs import Scattergl
import plotly.io as pio
import plotly.express as px
from core.singleton import SingletonMeta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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


class PlotContext(metaclass= SingletonMeta):
    def __init__(self, strategy: PlotStrategy):
        logging.info("Initializing PlotContext")
        self.strategy = strategy
        
    def _get_strategy(self, strategy_name: str, plot_subtype: str = None):
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

    def set_strategy(self, strategy_name: str,plot_subtype: str = None):
        self.strategy = self._get_strategy(strategy_name, plot_subtype)

    def update_plot(self, data, **kwargs):
        self.fig = Figure()
        self.fig= self.strategy.create_plot(self.fig, data, **kwargs)

    def set_plot(self, fig):
        self.fig = fig