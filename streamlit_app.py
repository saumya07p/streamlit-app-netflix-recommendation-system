import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.graph_objects as go
import requests
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_credentials():
        return st.secrets["GOOGLE_SHEETS_CREDS"]

def connect_to_google_sheets(user_data):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

        creds_dict = load_credentials()
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open(user_data).sheet1
        
        return sheet

def load_data(sheet):
        data = sheet.get_all_records()
        return pd.DataFrame(data)

st.set_page_config(layout='wide')

st.sidebar.image('https://i.ytimg.com/vi/gbbaX6WzBFg/maxresdefault.jpg')

ott=st.sidebar.selectbox('OTT Platform',['Home','Dashboard','Model1','Model2'])

def home():

    st.markdown("<h1 style='text-align: center;'>User collected responses: Google Data preview</h1>", unsafe_allow_html=True)
    SHEET_NAME = "user_data"
    sheet = connect_to_google_sheets(SHEET_NAME)
    df = load_data(sheet)
    st.write("Data from Google Sheets:")

    if 'Timestamp' in df.columns:
        df = df.drop('Timestamp', axis=1)

    df.rename(columns={'What is your age group?':'Age group',
                        'Which mode do you prefer to watch movies?': 'Preferred Mode',
                        'Which one of the following genres do you prefer to watch? (Select your top most favorite)': 'Favorite Genre',
                        'Which of the following do you use most frequently to choose a streaming platform?': 'Platform Choice Factor',
                        'On which devices do you primarily watch content?': 'Primary Device(to watch content)',
                        'How often do you watch or consume content from streaming platforms?': 'Watch Frequency',                 
                            'How satisfied are you with the recommendations you receive from streaming platforms?': 'Satisfaction Level',
                            'Are you satisfied with the recommendations you receive from streaming platforms?': 'Recommendation Satisfaction',
                            'What prevents you from using Netflix?': 'Netflix Barrier',
                            'How long do you spend each day watching content on streaming services?': 'Daily Watch Time',
                            'Does high subscription rate of one platform, forces you to switch to another platform?': 'Switching Due to Cost',
                            'Kindly give your preference':'Duration preference (season/hr wise)'},inplace=True)
        
    df.reset_index(drop=True, inplace=True)
        
    st.dataframe(df)

    columns_to_keep = st.multiselect("Select columns to keep:",options=df.columns)

    if columns_to_keep:
        df_filtered = df[columns_to_keep].copy()
        df_filtered.reset_index(drop=True, inplace=True)

        st.write("Selected column(s):")
        st.write(df_filtered)
    else:
        st.write("No columns selected.")

def dashboard():

    SHEET_NAME = "user_data"
    sheet = connect_to_google_sheets(SHEET_NAME)
    df = load_data(sheet)

    st.markdown("<h1 style='text-align: center;'>Netflix Recommendation System Dashboard</h1>", unsafe_allow_html=True)
   
    if 'Timestamp' in df.columns:
        df = df.drop('Timestamp', axis=1)

    FILE_ID = '1IigjkaGJeY_Dr1I1-mfDRyzIlDImw2rt'

    url = f'https://drive.google.com/uc?id={FILE_ID}&export=download'

    response = requests.get(url)
    data = pd.read_excel(BytesIO(response.content), engine='openpyxl')

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=data['Year'],
        y=data['Subscriptions'],
        mode='lines+markers',
        name='Subscription'
    ))

    fig1.add_hline(y=167.09, line_dash="dash", line_color="grey", annotation_text="COVID19 Start Year")
    fig1.add_hline(y=221.84, line_dash="dash", line_color="grey", annotation_text="COVID19 End Year")

    fig1.update_layout(
        title="Subscription Over Years",
        xaxis_title="Year",
        yaxis_title="Subscription")

    st.plotly_chart(fig1)

    df.rename(columns={'What is your age group?':'Age group',
                       'Which mode do you prefer to watch movies?': 'Preferred Mode',
                       'Which one of the following genres do you prefer to watch? (Select your top most favorite)': 'Favorite Genre',
                       'Which of the following do you use most frequently to choose a streaming platform?': 'Platform Choice Factor',
                       'On which devices do you primarily watch content?': 'Primary Device(to watch content)',
                       'How often do you watch or consume content from streaming platforms?': 'Watch Frequency',                 
                        'How satisfied are you with the recommendations you receive from streaming platforms?': 'Satisfaction Level',
                        'Are you satisfied with the recommendations you receive from streaming platforms?': 'Recommendation Satisfaction',
                        'What prevents you from using Netflix?': 'Netflix Barrier',
                        'How long do you spend each day watching content on streaming services?': 'Daily Watch Time',
                        'Does high subscription rate of one platform, forces you to switch to another platform?': 'Switching Due to Cost',
                        'Kindly give your preference':'Duration preference (season/hr wise)'},inplace=True)
    
    column_values = df['Preferred Mode']
    column_values_list = df['Preferred Mode'].tolist()
    df['Preferred Mode'] = df['Preferred Mode'].str.split(' - ').str[0]

    col1, col2 = st.columns((10,10))

    movie_loc = df['Preferred Mode'].value_counts()
    fig2 = go.Figure(data=[go.Bar(
        x=movie_loc.index,
        y=movie_loc.values,
        marker_color=['#ff4d4d', '#ff9999'] 
    )])

    fig2.update_layout(
        xaxis_title="Mode",
        yaxis_title="Count",
        title = {
        'text':'Preferred Modes of Watching Movies',
        'x': 0.3  
        } 
    )
    col1.plotly_chart(fig2)

    platform_preference = df['Platform Choice Factor'].value_counts()

    platform_df = platform_preference.reset_index()
    platform_df.columns = ['Platform', 'Count']

    platform_df = platform_df.sample(frac=1).reset_index(drop=True)

    fig3 = px.scatter(platform_df,
                    x="Platform", 
                    y="Count",
                    size="Count",
                    color="Count",
                    hover_name="Platform",
                    title="Platform Preference",
                    labels={"Platform": "Platform", "Count": "Count of Responses",
                    },
                    color_continuous_scale=[
                        "#ff9999",  # Light red
                        "#ff4d4d",  # Medium red
                        "#e60000",  # Dark red
                        "#990000"   # Deepest red
                    ],
                    size_max=70)

    fig3.update_layout(
        width=600,
        xaxis_tickangle=90,
        title={
        'text': 'Platform Preference',
        'y': 0.9,
        'x': 0.4,
        'xanchor': 'center',
        'yanchor': 'top'}
    )

    col2.plotly_chart(fig3)

    fig4 = px.histogram(df, 
                    x="Favorite Genre",
                    color="Gender",
                    category_orders={"Favorite Genre": df['Favorite Genre'].unique()},
                    title="Genre Preferences by Gender", 
                    labels={"Favorite Genre": "Genre Preference", "count": "Count of Users"},
                    barmode="stack",
                    )

    fig4.update_layout(
        title={
        'text': 'Platform Preference',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
    )

    st.plotly_chart(fig4)

    fig5 = px.bar(df, x = 'Favorite Genre',
                  title = 'Genre Count', 
                  color = 'Favorite Genre', 
                  color_continuous_scale=[
                    "#660000",  # Very dark red
                    "#800000",  # Dark red
                    "#990000",  # Red
                    "#b30000",  # Medium dark red
                    "#cc3333",  # Bright red
                    "#e60000",  # Strong red
                    "#ff6666",  # Light red
                    "#ff9999"   # Very light red
                    ])
    fig5.update_layout(
    xaxis_title='Genre',
    yaxis_title='Genre Count',
    xaxis_tickangle=90,
    title={
    'text': 'User preferred Genres',
    'y': 0.9,
    'x': 0.5,
    'xanchor': 'center',
    'yanchor': 'top'},
    xaxis={
        'categoryorder': 'total descending'
    }
   )
    col2.plotly_chart(fig5)

    df_sorted = df['Satisfaction Level'].value_counts().sort_values(ascending=False)

    fig6 = px.histogram(df,
                   x='Satisfaction Level',
                   color = 'Satisfaction Level',
                   nbins=6,
                   title='Streaming Recommendations Satisfaction',
                                color_discrete_sequence=[
                        "#8B0000",  # Dark red
                        "#B22222",  # Firebrick
                        "#DC143C",  # Crimson
                        "#FF6347",  # Tomato
                        "#FF9999"   # Light red
    ]
)

    fig6.update_layout(xaxis_title='Satisfaction Level',
                  yaxis_title='Count',
                   title={
        'text': 'Satisfaction with Streaming Recommendations',
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        xaxis={'categoryorder': 'total descending'}
        )
    col1.plotly_chart(fig6)

    movie_loc1 = df['Switching Due to Cost'].value_counts()
    fig7= go.Figure(data=[go.Bar(
        x=movie_loc1.index,
        y=movie_loc1.values,
        marker_color=['#1f77b4', '#ff7f0e']
    )])

    fig7.update_layout(
        title="Preferred Modes of Watching Movies",
        xaxis_title="Mode",
        yaxis_title="Count",
        xaxis={'categoryorder': 'total descending'}
    )

    st.plotly_chart(fig7)

    col3, col4 = st.columns((10,10))

    ratings=df['Daily Watch Time'].value_counts()
    ratings_df = pd.DataFrame(ratings).reset_index()
    ratings_df.columns = ['Watch Hours', 'Count']
    col3.dataframe(ratings_df, use_container_width=True)

    # html_table = ratings_df.to_html(index=False, justify='center', border=0)

    # col5, col6 = st.columns([2,2])

    # with col5:
    #     st.markdown("<h3 style='text-align: center;'>Daily Watch Time Statistics</h3>", unsafe_allow_html=True)

    #     styled_df = ratings_df.style.set_table_styles(
    #         [
    #         {"selector": "th", "props": [("text-align", "center"), ("font-size", "16px"), ("font-weight", "bold")]},  # Center header and style
    #         {"selector": "td", "props": [("text-align", "center"), ("padding", "8px")]}  # Center table data and add padding
    #         ]
    #     )

    # with col5:
    #     st.table(styled_df)

    pair_counts = df.groupby(['Watch Frequency', 'Daily Watch Time']).size().reset_index(name='count')
    pair_counts.sort_values(by='count',ascending=False).head(3)
    col4.dataframe(pair_counts, use_container_width=True)

def model1():

    st.title('Content based Movie Recommendation System')

    file_id2 = '1SoHSIAK4Mx9QNjwxaJQ0WNcwvOD6ioJT'

    url = f'https://drive.google.com/uc?id={file_id2}'

    movies_df1 = pd.read_csv(url, encoding='latin1')

    st.write('A Content-Based Recommendation System is a type of recommendation system that suggests items to users based on the features or characteristics of the items themselves, rather than user behavior or interactions (which is the case in collaborative filtering). The system analyzes the content or attributes of the items and recommends similar items that match the user past preferences.')

    xyz = movies_df1['Genre'].unique()
    recomm1 = st.selectbox('Select your Preferred Genre', xyz)

    def reco(genre):
        filter=movies_df1[movies_df1['Genre']==genre]
        filter_final=filter.sort_values(by='IMDB Score', ascending= False)
        filter_final.reset_index(inplace=True)
        filter_final=filter_final[['Title','Runtime','IMDB Score']]
        filter_final=filter_final.head(10)
        # filter_final.drop('index', inplace=True)
        return filter_final
    
    movies_list=reco(recomm1)
    st.dataframe(movies_list, use_container_width=True)
    st.write("We are currently in the process of collecting data for our academic research project, and your participation would be incredibly valuable to us. By completing this form, you will contribute to the success of our study, and we would greatly appreciate your time and input. Your responses will help us gain insights that are essential for our research. Thank you in advance for your effort and support! : You can access the Google Form by clicking on the link below:")
    st.page_link('https://forms.gle/ZDd8UQP9qVykxMz99', label = 'https://forms.gle/ZDd8UQP9qVykxMz99')

def model2():

    file_id = '1hc3q0Kt7SK-QCrL5Az-jpDJdKtaYrQda'

    url = f'https://drive.google.com/uc?id={file_id}'

    movies_df = pd.read_csv(url)
    
    st.title('Context Based Movie Recommendation System')
    st.write('Description-based recommendation uses the textual content of movie descriptions to find similarities between movies. It compares the description of a given movie with others using techniques like TF-IDF and cosine similarity to quantify how similar they are. The system then suggests the top 10 movies with the most similar descriptions to the input movie.')

    abc = movies_df['title'].unique()
    recomm = st.selectbox('Select your Preferred Movie', abc)

    movies_df = movies_df[['title', 'cast', 'description']].fillna('')

    movies_df['combined_features'] = movies_df['cast'] + " " + movies_df['description']

    tfidf = TfidfVectorizer(stop_words='english')

    tfidf_matrix = tfidf.fit_transform(movies_df['combined_features'])

    # Compute cosine similarity matrix based on the combined features
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Function to recommend movies based on title input
    def recommend_movies(movie_title, cosine_sim=cosine_sim):
        # Get the index of the movie that matches the title
        idx = movies_df[movies_df['title'] == movie_title].index[0]
        
        # Get pairwise similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))
        
        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]  # Exclude the first one as it is the same movie
        
        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Return the top 10 most similar movies
        return movies_df['title'].iloc[movie_indices]

    recommendations = recommend_movies(recomm)
    df_movies = pd.DataFrame(recommendations).reset_index()
    df_movies.drop('index', axis = 1, inplace =True)
    st.dataframe(df_movies, use_container_width=True)

    st.write("We are currently in the process of collecting data for our academic research project, and your participation would be incredibly valuable to us. By completing this form, you will contribute to the success of our study, and we would greatly appreciate your time and input. Your responses will help us gain insights that are essential for our research. Thank you in advance for your effort and support! : You can access the Google Form by clicking on the link below:")
    st.page_link('https://forms.gle/ZDd8UQP9qVykxMz99', label = 'https://forms.gle/ZDd8UQP9qVykxMz99')
    
if ott=='Home':
    home()
elif ott=='Dashboard':
     dashboard()
elif ott == 'Model1':
    model1()
elif ott == 'Model2':
    model2()