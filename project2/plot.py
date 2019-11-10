import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
dumby
544, 544, 542
0.0685, 0.1969, 0.10
183, 525, 277

greedy
560, 560, 560
0,052,  0,1483, 0,0459
117, 362, 117

smarty
560, 560, 560
0.1436, 0,2291, 0,1366
117, 362, 117
"""



dumby = [183, 525, 249]
greedy = [117, 362, 117]
smarty = [117, 362, 117]

index = ['hminimax0', 'himinimax1', 'hminimax2']
df = pd.DataFrame({'dumby': dumby, 'greedy': greedy,
                   'smarty': smarty}, index=index)

ax = df.plot.bar(rot=0)
# plt.ylabel('Score')
# plt.ylabel('Computation time')
plt.ylabel('Number of expanded nodes')


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
        label = "{:.1f}".format(y_value)

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
