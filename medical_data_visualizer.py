import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv",header=0)

# Add 'overweight' column
df['overweight'] =df.apply(lambda row: 1 if (row["weight"]/(row["height"]/100)**2)>25 else 0,axis=1)


# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
medical_dict = { 1: 0, 2 : 1, 3: 1}

df['cholesterol'] = df['cholesterol'].map( medical_dict )

df['gluc'] = df['gluc'].map( medical_dict ) 

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = None


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat = df.groupby(['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke','cardio']).size().rename("total").reset_index().melt(['total', 'cardio'])

    # Draw the catplot with 'sns.catplot()'
    fig=plt.gcf()
    sns.catplot(data = df_cat, x='variable', y='total', hue='value', col='cardio', kind="bar", ci = None)
    

    # Do not modify the next two lines
    fig.savefig('catplot.png')

    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat=df.copy(deep=True)
    df_heat.drop(df[(df['ap_lo'] > df['ap_hi']) | (df['height'] < df['height'].quantile(0.025)) | (df['height'] >= df['height'].quantile(0.975)) | (df['weight'] < df['weight'].quantile(0.025)) | (df['weight'] >= df['weight'].quantile(0.975))].index,inplace=True)

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))


    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask,annot=True, fmt=".1f", vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
