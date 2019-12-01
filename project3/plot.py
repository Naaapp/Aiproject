import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
layout large_filter

confused = [5.253, 5.235, 5.625]
afraid = [2.205, 1.989, 2.292]
scared = [0.745, 0.735, 0.741]

layout large_filter_walls

confused = [4.274, 3.995, 4.650]
afraid = [2.455, 1.517, 2.531]  # seed = 2 the ghost go in the down right corner
scared = [0.835, 0.745, 0.765]
"""

confused = [4.274, 3.995, 4.650]
afraid = [2.455, 1.517, 2.531]  # seed = 2 the ghost go in the down right corner
scared = [0.835, 0.745, 0.765]

index = ['seed = 1', 'seed = 2', 'seed = 3']
df = pd.DataFrame({'confused': confused, 'afraid': afraid,
                   'scared': scared}, index=index)

ax = df.plot.bar(rot=0)
plt.ylabel('Error')


def add_value_labels(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.3f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,  # Use `label` as label
            (x_value, y_value),  # Place label at end of the bar
            xytext=(0, space),  # Vertically shift label by `space`
            textcoords="offset points",
            # Interpret `xytext` as offset in points
            ha='center',  # Horizontally center label
            va=va)  # Vertically align label differently for
        # positive and negative values.


# Call the function above. All the magic happens there.
add_value_labels(ax)

plt.show()
