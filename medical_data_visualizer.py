#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data.
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column.
df['bmi'] = df['weight'] / ((df['height'] / 100)**2)
df['overweight'] = df.apply(lambda row: 1 if row.bmi > 25 else 0, axis=1)

# Normalize data by making 0 always good and 1 always bad. If the
# value of 'cholestorol' or 'gluc' is 1, make the value 0. If the
# value is more than 1, make the value 1.
df['gluc'] = df.apply(lambda row: 0 if row.gluc == 1 else 1, axis=1)
df['cholesterol'] = df.apply(lambda row: 0 if row.cholesterol == 1 else 1, axis=1)


# Draw categorical plot.
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the
    # values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active',
    # and 'overweight'.
    df_cat = df.loc[:, ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight', 'cardio']].melt(id_vars=['cardio'])

    # Group and reformat the data to split it by 'cardio'. Show the
    # counts of each feature. You will have to rename one of the
    # columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='totals')

    # Draw the catplot with sns.catplot().
    fig = sns.catplot(data=df_cat, kind="bar", x="variable", y="totals", hue="value", col='cardio')

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# Draw heat map.
def draw_heat_map():
    # Clean the data.
    df_heat = df.loc[:, ['id', 'age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio', 'overweight']]
    # print(df_heat.head(30))

    # Calculate the correlation matrix.
    corr = df_heat.corr()

    # Generate a mask for the upper triangle.
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure.
    fig, ax = plt.subplots(figsize=(9, 9))

    # Draw the heatmap with sns.heatmap().
    ax = sns.heatmap(data=corr, mask=mask, square=True, annot=True, fmt='.1f')

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
