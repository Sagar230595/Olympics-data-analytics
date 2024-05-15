import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy as sc


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

st.sidebar.title("Olympics")
st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTH7E_YcFJi2zbxjhYoWLfl0Q2ZU3IBJgvbs9pUXGtbgg&s")

df = preprocessor.preprocess(df, region_df)

user_menu = st.sidebar.radio(
    'Select an Option',
    ("Medal Tally", "Overall Analysis", "Country-wise Analysis", "Athlete wise Analysis")
)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)

    selected_years = st.sidebar.selectbox("Select years", years)
    selected_country = st.sidebar.selectbox("Select country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_years, selected_country)

    if selected_years == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_years != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in year " + str(selected_years) + " Olympics")
    if selected_years == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance")
    if selected_years != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Performance in " + str(selected_years) + " Olympics")
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    Participating_nations = df['region'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Events")
        st.title(events)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Sports")
        st.title(sports)
    with col2:
        st.header("Nations")
        st.title(Participating_nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Editions", y="region")
    st.header("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Editions", y="Event")
    st.header("Number of events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Editions", y="Name")
    st.header("Number of Athletes over the years")
    st.plotly_chart(fig)

    st.title("No of Events over time (Every Sport)")
    fig,ax = plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athlete")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    selected_sport = st.selectbox('Select a sport', sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)


if user_menu == "Country-wise Analysis":
    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.header("Medal tally over the years for "+selected_country)
    st.plotly_chart(fig)

    st.header(selected_country + " excels in the following sports")
    pivot_table = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(25, 25))
    ax = sns.heatmap(pivot_table.astype('int'),annot=True)
    st.pyplot(fig)

    st.header("top 10 athletes of " + selected_country)
    top10_df = helper.most_succesful_athlete(df,selected_country)
    st.table(top10_df)


if user_menu == "Athlete wise Analysis":

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ["Age Distribution", "Age of Gold Medalist", "Age of Silver Medalist",
                                                "Age of Bronze Medalist"], show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    sport_name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        sport_name.append(sport)

    fig = ff.create_distplot(x, sport_name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt sports (Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    st.title("Height Vs Weight of Athletes")
    selected_sport = st.selectbox('Select a sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots(figsize=(12, 12))
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=50)
    st.pyplot(fig)

    final_df = helper.men_vs_women(df)
    fig = px.line(final_df, 'Year', ['Male', 'Female'])
    st.header("Men and Women Participation on Olympics over the Year")
    st.plotly_chart(fig)


