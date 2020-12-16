#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Import data.
df = pd.read_csv("medical_examination.csv")

# Add 'bmi' and 'overweight' column.
df["bmi"] = df["weight"] / ((df["height"] / 100.0) ** 2)
df["overweight"] = df["bmi"].apply(lambda item: 1 if item > 25 else 0)

# Massage all good values to 0, and all bad to 1.
# See README.md for further details.
df["gluc"] = df["gluc"].apply(lambda item: 0 if item == 1 else 1)
df["cholesterol"] = df["cholesterol"].apply(lambda item: 0 if item == 1 else 1)


# Draw categorical plot.
def draw_cat_plot():
    # For this plot, the correct data must be selected and then
    # organized for a bar chart.  Looking at examples/Figure_1.png
    # will help you to understand what variables are needed and in
    # what structure.  We want two separate bar charts, one with data
    # for which cardio = 0 and one for cardio = 1.  Each chart has an
    # x axis of 'variables' and a y axis of 'total.'  The bars are
    # colored according to the binary value of each category and the
    # bar height is the frequency of that data (how many times was the
    # active category equal to 1 for group cardio = 0?).

    # Select the data for the bar chart.  See examples/Figure_1.png
    # for the categories.
    df1 = df[["cholesterol", "gluc", "smoke", "alco", "active", "overweight", "cardio"]]

    # pd.melt() takes an ID variable.  Use 'cardio' since we intend to
    # group by it later.  This rearranges our table from rows
    # describing patient measurements to a long form table with
    # columns of cardio, variable (categories), and value.  This
    # already looks easier to convert to frequency data for a bar
    # chart.
    df1 = df1.melt(id_vars=["cardio"])

    # Since the bar charts are split by the separate 'cardio' values
    # and show the counts of each value for each category, we need to
    # group by 'cardio,' 'variable,', and 'value.'  Then we can count
    # the frequencies and name the new column 'total' to correspond to
    # the y axis of the bar chart.

    # Generate the groupby object to split by cardio value.
    df1 = df1.groupby(["cardio", "variable", "value"])

    # Compute the frequency of each category.
    df1 = df1.size()

    # Reset the index and name it 'total.'
    df1 = df1.reset_index(name="total")

    # If you print the data now, it will look very much like frequency
    # data for a bar chart.

    # Draw the catplot with sns.catplot().  To get the testing to
    # work, test_module.py needs access to the axes, which is accessed
    # by via sns.catplot().fig.  The parameters are fairly
    # self-explanatory.
    graph = sns.catplot(
        data=df1, kind="bar", x="variable", y="total", hue="value", col="cardio"
    )
    fig = graph.fig

    fig.savefig("catplot.png")
    return fig


# Draw heat map.
def draw_heat_map():
    # For this plot, all the calculations are done by our libraries.
    # Once cleaning is finished, the correlation coefficients are
    # computed by pandas.corr().

    # Clean the data.
    # Select the data for the heat map.  See examples/Figure_2.png for
    # the categories.
    df2 = df.loc[
        :,
        [
            "id",
            "age",
            "gender",
            "height",
            "weight",
            "ap_hi",
            "ap_lo",
            "cholesterol",
            "gluc",
            "smoke",
            "alco",
            "active",
            "cardio",
            "overweight",
        ],
    ]

    # Remove the outliers according to README.md.  Keep the data with
    # diastolic pressure lower than systolic (probably should be < and
    # not <=).  df['ap_lo'] <= df['ap_hi'] Discard heights outside the
    # 2.5 percentiles.
    #
    # NOTE: You must calculate the quantiles with the original data
    # frame as the quantiles will change as you eliminate data.
    #
    # df['height'] >= df['height'].quantile(0.025)
    # df['height'] <= df['height'].quantile(0.975)
    # df['weight'] >= df['weight'].quantile(0.025)
    # df['weight'] <= df['weight'].quantile(0.975)

    df2 = df2.loc[
        (df["ap_lo"] < df["ap_hi"])
        & (df["height"] >= df["height"].quantile(0.025))
        & (df["height"] <= df["height"].quantile(0.975))
        & (df["weight"] >= df["weight"].quantile(0.025))
        & (df["weight"] <= df["weight"].quantile(0.975))
    ]

    # Calculate the correlation matrix.  This calculates a
    # variable-variable correlation, as in height-weight (or, does the
    # height data have some relationship with the weight data?).
    corr = df2.corr()

    # Generate a mask.  np.triu makes an upper triangular matrix from
    # corr, zeroing all values on the diagonal and below.  Pandas will
    # then mask, or ignore, all values in the mask that are truthy
    # (above the diagonal) for the upper triangle.
    mask = np.triu(corr)

    # Set up the matplotlib figure.  This makes the plot larger than
    # the example.
    fig, ax = plt.subplots(figsize=(9, 9))

    # Draw the heatmap with sns.heatmap(), and store in ax for
    # testing.  'annot' generates labels, and '.1f' sets the number
    # format for the labels.
    ax = sns.heatmap(data=corr, mask=mask, square=True, annot=True, fmt=".1f")
    ax.has_data()

    fig.savefig("heatmap.png")
    return fig
