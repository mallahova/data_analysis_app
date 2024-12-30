# from core.readers import FileReaderFactory
# from core.transformers import DataBuilder
# from core.strategies import PlotFactory
# from core.dashboard import Dashboard


# class Client:
#     """Client class to handle the entire data visualization workflow."""

#     def __init__(self):
#         self.reader_factory = FileReaderFactory()
#         self.plot_factory = PlotFactory()
#         self.dashboard = Dashboard()
#         self.data = None

#     # Step 1: Read Data
#     def read_data(self, file_type, source, **kwargs):
#         """
#         Reads data using the appropriate reader.
#         Args:
#             file_type (str): Type of file (e.g., 'csv', 'json').
#             source (str): Path or URL to the data source.
#             kwargs: Additional parameters for the specific reader.
#         """
#         reader = self.reader_factory.get_reader(file_type)
#         self.data = reader.read(source, **kwargs)
#         print(f"Data loaded successfully from {source}.")

#     # Step 2: Transform Data
#     def transform_data(self, transformations):
#         """
#         Applies a series of transformations to the data.
#         Args:
#             transformations (list of tuples): Each tuple represents a method and its arguments.
#                                                Example: [("filter_columns", ["col1", "col2"]),
#                                                          ("normalize_column", "col1")]
#         """
#         if self.data is None:
#             raise ValueError("No data loaded. Please load data first using `read_data`.")
#         builder = DataBuilder(self.data)
#         for method, args in transformations:
#             if isinstance(args, (list, tuple)):
#                 builder = getattr(builder, method)(*args)
#             else:
#                 builder = getattr(builder, method)(args)
#         self.data = builder.build()
#         print("Data transformations applied successfully.")

#     # Step 3: Add Plots
#     def add_plot(self, plot_type, **kwargs):
#         """
#         Adds a plot to the dashboard.
#         Args:
#             plot_type (str): Type of plot (e.g., 'scatter', 'line').
#             kwargs: Plot-specific parameters (e.g., x, y, color, etc.).
#         """
#         if self.data is None:
#             raise ValueError("No data loaded. Please load data first using `read_data`.")
#         plot_strategy = self.plot_factory.get_plot(plot_type)
#         self.dashboard.add_plot(plot_strategy, self.data, **kwargs)
#         print(f"{plot_type.capitalize()} plot added to the dashboard.")

#     # Step 4: Render Dashboard
#     def render_dashboard(self):
#         """
#         Renders all the plots in the dashboard.
#         """
#         if not self.dashboard.plots:
#             print("Dashboard is empty. Add plots before rendering.")
#         else:
#             self.dashboard.render()
#             print("Dashboard rendered successfully.")
