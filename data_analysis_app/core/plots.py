from abc import ABC, abstractmethod
from plotly.graph_objects import Figure, Scatter, Histogram, Heatmap, Box

class PlotStrategy(ABC):
    @abstractmethod
    def create_plot(self, data, title: str, **kwargs) -> Figure:
        """Creates a plot based on the provided data and parameters."""
        pass


class LinePlotStrategy(PlotStrategy):
    def create_plot(self, data, title: str, x_column, y_column, line_color="blue", line_width=2):
        fig = Figure()
        fig.add_trace(Scatter(x=data[x_column], y=data[y_column], mode="lines",
                              line=dict(color=line_color, width=line_width)))
        fig.update_layout(title=title, xaxis_title=x_column, yaxis_title=y_column)
        return fig


class ScatterPlotStrategy(PlotStrategy):
    def create_plot(self, data, title: str, x_column, y_column, marker_symbol="circle", marker_color="red"):
        fig = Figure()
        fig.add_trace(Scatter(x=data[x_column], y=data[y_column], mode="markers",
                              marker=dict(symbol=marker_symbol, color=marker_color)))
        fig.update_layout(title=title, xaxis_title=x_column, yaxis_title=y_column)
        return fig


class HistogramStrategy(PlotStrategy):
    def create_plot(self, data, title: str, x_column, bins=30, bar_color="green"):
        fig = Figure()
        fig.add_trace(Histogram(x=data[x_column], nbinsx=bins, marker=dict(color=bar_color)))
        fig.update_layout(title=title, xaxis_title=x_column)
        return fig


class HeatmapStrategy(PlotStrategy):
    def create_plot(self, data, title: str, z_data, colorscale="Viridis"):
        fig = Figure()
        fig.add_trace(Heatmap(z=z_data, colorscale=colorscale))
        fig.update_layout(title=title)
        return fig


class BoxPlotStrategy(PlotStrategy):
    def create_plot(self, data, title: str, y_column, box_color="orange"):
        fig = Figure()
        fig.add_trace(Box(y=data[y_column], marker=dict(color=box_color), boxmean="sd"))
        fig.update_layout(title=title, yaxis_title=y_column)
        return fig


class PlotContext:
    def __init__(self, strategy: PlotStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PlotStrategy):
        self.strategy = strategy

    def create_plot(self, data, title: str, **kwargs):
        return self.strategy.create_plot(data, title, **kwargs)
