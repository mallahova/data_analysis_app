from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Iterator


class PlotObserver(ABC):
    @abstractmethod
    def update_color(self, color: str):
        """Update the color of the plot when notified."""
        pass


class Plot(PlotObserver):
    def __init__(self, title: str, figure, plot_type: str):
        self.title = title
        self.figure = figure
        self.plot_type = plot_type
        self.color = None  # Default color

    def update_color(self, color: str):
        """Updates the color of the plot when notified by the Dashboard."""
        self.color = color
        self.figure.update_traces(
            marker_color=color if self.plot_type in ["scatter", "histogram", "boxplot"] else None,
            line_color=color if self.plot_type == "line" else None,
        )

    def __str__(self):
        return f"{self.plot_type.capitalize()} Plot: {self.title}"


class Dashboard:
    def __init__(self):
        self.plots: List[Plot] = []
        self.observers: List[PlotObserver] = []

    def add_plot(self, plot: Plot):
        """Adds a plot to the dashboard and registers it as an observer."""
        self.plots.append(plot)
        self.observers.append(plot)

    def change_color_theme(self, color: str):
        """Notifies all plots (observers) to update their colors."""
        for observer in self.observers:
            observer.update_color(color)

    def get_iterator(self, strategy: str) -> Iterator[Plot]:
        """Creates an iterator based on the given strategy."""
        if strategy == "by_type":
            return PlotTypeIterator(self.plots)
        elif strategy == "alphabetical":
            return AlphabeticalIterator(self.plots)
        else:
            raise ValueError(f"Unknown iteration strategy: {strategy}")

    def __str__(self):
        return f"Dashboard with {len(self.plots)} plots."


class PlotIterator(ABC):
    @abstractmethod
    def __iter__(self) -> "PlotIterator":
        pass

    @abstractmethod
    def __next__(self) -> Plot:
        pass


class PlotTypeIterator(PlotIterator):
    def __init__(self, plots: List[Plot]):
        self.type_order = defaultdict(list)
        for plot in plots:
            self.type_order[plot.plot_type].append(plot)
        self.plot_types = iter(sorted(self.type_order.keys()))
        self.current_type = None
        self.index = 0

    def __iter__(self) -> "PlotTypeIterator":
        return self

    def __next__(self) -> Plot:
        if self.current_type is None or self.index >= len(self.type_order[self.current_type]):
            self.current_type = next(self.plot_types)  # Move to the next plot type
            self.index = 0

        plot = self.type_order[self.current_type][self.index]
        self.index += 1
        return plot


class AlphabeticalIterator(PlotIterator):
    def __init__(self, plots: List[Plot]):
        self.sorted_plots = sorted(plots, key=lambda p: p.title)
        self.index = 0

    def __iter__(self) -> "AlphabeticalIterator":
        return self

    def __next__(self) -> Plot:
        if self.index >= len(self.sorted_plots):
            raise StopIteration
        plot = self.sorted_plots[self.index]
        self.index += 1
        return plot
