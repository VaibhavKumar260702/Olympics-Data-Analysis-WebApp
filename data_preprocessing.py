import pandas as pd


def data_preprocessing(df, region_df):
    df = df[df['Season'] == 'Summer']  # taking only summer olympics
    df = df.merge(region_df, on='NOC', how='left')  # merging two csv on NOC
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)  # one hot encoding medals

    return df
