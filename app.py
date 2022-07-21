import streamlit as st
import pandas as pd
import data_preprocessing, functions
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = data_preprocessing.data_preprocessing(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image(
    'https://99designs-blog.imgix.net/blog/wp-content/uploads/2018/02/900px-Olympic_flag.svg.png?auto=format&q=60&fit=max&w=930')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Count', 'Overall Analysis', 'Country-wise Analysis', 'Players Statistics')
)

if user_menu == 'Medal Count':
    st.sidebar.header("Medal Count")
    years, country = functions.country_year_list(df)

    selected_country = st.sidebar.selectbox("Select Country", country)
    selected_year = st.sidebar.selectbox("Select Year", years)

    medal_count = functions.medal_count(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Count")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Count in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + "'s performance in " + str(selected_year) + " Olympics")
    st.table(medal_count)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    players = df['Name'].unique().shape[0]
    countries = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Editions")
        st.title(editions)
    with col2:
        st.subheader("Hosts")
        st.title(cities)
    with col3:
        st.subheader("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Events")
        st.title(events)
    with col2:
        st.subheader("Countries")
        st.title(countries)
    with col3:
        st.subheader("Players")
        st.title(players)

    nations_over_time = functions.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Countries over the years")
    st.plotly_chart(fig)

    events_over_time = functions.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = functions.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Players over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over years")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    st.title("Most successful Players")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = functions.most_decorated(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    default_idx = 80
    selected_country = st.sidebar.selectbox('Select a Country', country_list, index=default_idx)

    country_df = functions.yearwise_medal_count(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + "'s Medal Count over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = functions.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 Players of " + selected_country)
    top10_df = functions.most_decorated_country_wise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Players Statistics':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = df.drop_duplicates(subset=['Name', 'region'])['Age'].dropna()
    medal_df = df.dropna(subset=['Medal'])
    x2 = medal_df[medal_df['Medal'] == "Gold"]['Age'].dropna()
    x3 = medal_df[medal_df['Medal'] == "Silver"]['Age'].dropna()
    x4 = medal_df[medal_df['Medal'] == "Bronze"]['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=850, height=600)
    st.title("Distribution of Player's Age")
    st.plotly_chart(fig)

    x = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    famous_sports.sort()
    st.title("Distribution of Age wrt Sport (Gold Medalist)")
    selected_sport_for_stats = st.selectbox('Select a Sport', famous_sports)
    temp_df = medal_df[medal_df['Sport'] == selected_sport_for_stats]
    x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())

    fig = ff.create_distplot(x, [selected_sport_for_stats], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=850, height=600)

    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight (Gold)')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = functions.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Sex'], s=30)
    st.pyplot(fig)

    st.title("Men Vs Women Participation over the Years")
    final =functions.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=850, height=600)
    st.plotly_chart(fig)
