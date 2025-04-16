import matplotlib.pyplot as plt
import re
import os

def create_aggregated_plot(dataframes, output_dir: str):
    """
    Create scatter plots for each sensor data column in Vehicle Diagnostic logs.

    :param dataframes: List of pandas dataframes containing VDA log data.
    :param output_dir: The directory where the final plots will be stored.
    :return: None
    """

    # Identify the dataframe with the most columns to ensure complete plotting.
    largest_column_list = max([df.columns.tolist() for df in dataframes], key=len)

    # First column in Vehicle Diagnostic data is assumed to be Time (s).
    for column in largest_column_list[1:]:
        for df in dataframes:
            if column in df.columns:
                plt.scatter(df['Time (s)'], df[column], s=1)

        plt.title(f"{column} Over Time")
        plt.xlabel("Time (s)")
        plt.ylabel(column)
        output_filename = os.path.join(output_dir, re.sub(r'\W', "", column) + ".svg")
        plt.savefig(output_filename)
        plt.clf()
