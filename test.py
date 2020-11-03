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

# Narrow the data set. 
# df1 = df.loc[:, ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight', 'cardio']]
# df1 = df1.melt(id_vars=['cardio'])

# # Regroup by 'cardio' and sum.
# df1 = df1.groupby(['cardio', 'variable', 'value'])
# df1 = df1.size()
# df1 = df1.reset_index(name='totals')

# # Draw the catplot with sns.catplot().
# fig = sns.catplot(data=df1, kind="bar", x="variable", y="totals", hue="value", col='cardio')

# # Do not modify the next two lines
# fig.savefig('catplot.png')
# return fig

# Draw heat map.
# def draw_heat_map():
# Clean the data.
df1 = df.loc[:,
                [
                    'id',
                    'age',
                    'gender',
                    'height',
                    'weight',
                    'ap_hi',
                    'ap_lo',
                    'cholesterol',
                    'gluc',
                    'smoke',
                    'alco',
                    'active',
                    'cardio',
                    'overweight',
                ]
]

df1 = df1.loc[df['ap_lo'] <= df['ap_hi']]
df1 = df1.loc[df['height'] >= df['height'].quantile(0.025)]
df1 = df1.loc[df['height'] <= df['height'].quantile(0.975)]
df1 = df1.loc[df['weight'] >= df['weight'].quantile(0.025)]
df1 = df1.loc[df['weight'] <= df['weight'].quantile(0.975)]

df2 = df.loc[:,
                [
                    'id',
                    'age',
                    'gender',
                    'height',
                    'weight',
                    'ap_hi',
                    'ap_lo',
                    'cholesterol',
                    'gluc',
                    'smoke',
                    'alco',
                    'active',
                    'cardio',
                    'overweight',
                ]
]

df2 = df2.loc[
    (df['ap_lo'] <= df['ap_hi'])
    & (df['height'] >= df['height'].quantile(0.025))
    & (df['height'] <= df['height'].quantile(0.975))
    & (df['weight'] >= df['weight'].quantile(0.025))
    & (df['weight'] <= df['weight'].quantile(0.975))
]

print(df1.shape)
print(df2.shape)

# Calculate the correlation matrix.
# corr = df2.corr()

# Generate a mask for the upper triangle.
# mask = np.triu(corr)

# Set up the matplotlib figure.
# fig, ax = plt.subplots(figsize=(9, 9))

# Draw the heatmap with sns.heatmap().
# ax = sns.heatmap(data=corr, mask=mask, square=True, annot=True, fmt='.1f')

# Do not modify the next two lines
# fig.savefig('heatmap.png')
# return fig
