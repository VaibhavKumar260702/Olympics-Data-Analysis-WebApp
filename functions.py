import numpy as np
import pandas as pd


def medal_count(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp_df = medal_df
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']]
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']]

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')

    if flag==1:
        x=x.sort_values('Year').reset_index()
    else:
        x = x.sort_values(by=['Total', 'Gold'], ascending=False).reset_index()
    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return nations_over_time


def most_decorated(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    temp_df = temp_df.groupby('Name').sum()[['Gold', 'Silver', 'Bronze']].reset_index()
    temp_df['Total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    temp_df = temp_df.sort_values(by=['Total', 'Gold', 'Silver', 'Bronze'], ascending=False)
    x = pd.merge(temp_df, df[['Name', 'Sport', 'region', 'Medal']].dropna(subset=['Medal']), on='Name')
    x = x[['Name', 'Total', 'Gold', 'Silver', 'Bronze', 'Sport', 'region']].drop_duplicates('Name')
    x = x.head(15)
    return x.reset_index(drop=True)


def yearwise_medal_count(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_decorated_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    temp_df = temp_df.groupby(['Name']).sum()[['Gold', 'Silver', 'Bronze']].reset_index()
    temp_df['Total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    temp_df = temp_df.sort_values(by=['Total', 'Gold', 'Silver', 'Bronze'], ascending=False)
    x = pd.merge(temp_df, df[['Name', 'Sport', 'region', 'Medal']].dropna(subset=['Medal']), on='Name')
    x = x[['Name', 'Total', 'Gold', 'Silver', 'Bronze', 'Sport', 'region']].drop_duplicates('Name')
    x = x.head(10)
    return x.reset_index(drop=True)


def weight_v_height(df, sport):
    athlete_df = df.dropna(subset=['Medal'])
    athlete_df=athlete_df[athlete_df['Gold']!=0]
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
