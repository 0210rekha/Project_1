#import libraries
import googleapiclient.discovery
import pandas as pd
import mysql.connector
import time
import streamlit as st
import datetime
from streamlit_option_menu import option_menu
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

#API key connection to interact with youtube API
def connect_api_key():
    api_key="AIzaSyBHotD9qOozs5MZvVhpCQbmAlQMQaozIGE"
    api_service_name = "youtube"
    api_version = "v3"
    youtube=googleapiclient.discovery.build(api_service_name,
    api_version,developerKey=api_key)
    return youtube
youtube=connect_api_key()

# Function to retrieve channel details from YouTube
def get_channal_info(channel_id):
        LIST_DATA=[]
        request = youtube.channels().list(
            part="contentDetails,snippet,statistics",
            id=channel_id
        )
        response=request.execute()
        for i in response['items']:
                data=dict(channel_name=i['snippet']['title'],
                channel_id=i['id'],
                subscribers=i['statistics']['subscriberCount'],
                viewscount=i['statistics']['viewCount'],
                description=i['snippet']['description'],
                playlist_id=i['contentDetails']['relatedPlaylists']['uploads'])
                LIST_DATA.append(data)

        return LIST_DATA

# Function to retrieve Video_ids from YouTube with help of channel_id
def get_video_id(channel_id):
    Video_ids=[]
    try:
        request=youtube.channels().list(part="contentDetails",
                                        id=channel_id)
        response=request.execute()
        playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token=None
        while True:
            request_video=youtube.playlistItems().list(part="contentDetails,snippet",
                                                    playlistId= playlist_id,
                                                    maxResults=50,
                                                pageToken=next_page_token)
            response_video=request_video.execute()
            for i in range(len(response_video['items'])):
                data_1=response_video['items'][i]['snippet']['resourceId']['videoId']
                Video_ids.append(data_1)
            next_page_token=response_video.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return Video_ids

# Function to retrieve video details from YouTube
def time_duration(t):
            a = pd.Timedelta(t)
            b = str(a).split()[-1]
            return b
def get_video_info(Video_ids):
    video_data=[]
    try:
        for video_id in Video_ids:
            resquest_videoid=youtube.videos().list(
                part='contentDetails,snippet,statistics',
                id=video_id
            )            
            response_videoid=resquest_videoid.execute()
            for i in response_videoid['items']:
                data2=dict(Video_id=i['id'],
                            video_name=i['snippet']['title'],
                            channel_name=i['snippet']['channelTitle'],
                            video_description=i['snippet']['description'],
                            PublishedAt=i['snippet']['publishedAt'].replace("T"," ").replace("Z"," "),
                            view_count=i['statistics']['viewCount'],
                            like_count=i['statistics']['likeCount'],
                            Favorite_count=i['statistics']['favoriteCount'],
                            comment_count=i['statistics']['commentCount'],
                            duration=time_duration(i['contentDetails']['duration']),
                            Thumbnail=i['snippet']['thumbnails']['default']['url'],
                            caption_status=i['contentDetails']['caption'] )
            video_data.append(data2)
    except:
        pass
    return video_data

# Function to retrieve comments details from YouTube
def get_comment_info(Video_ids):
    video_comments=[]
    try:
        for video_id in Video_ids:
            request_comment = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id
            )
            response_comment=request_comment.execute()
            for i in response_comment['items']:
                data_3=dict(comment_id=i['snippet']['topLevelComment']['id'],
                            comment_text=i['snippet']['topLevelComment']['snippet']['textDisplay'],
                            comment_authour=i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            comment_publishedat=i['snippet']['topLevelComment']['snippet']['publishedAt'].replace("T"," ").replace("Z"," "))
                video_comments.append(data_3)
    except:
        pass
    return video_comments

# Function to retrieve playlists details from YouTube
def get_playlist_info(channel_id):
    playlist=[]
    try:
        next_page_token=None
        while True:
            request_playlist=youtube.playlists().list(
                part="contentDetails,snippet",
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response_playlist=request_playlist.execute()

            for i in response_playlist['items']:
                data_4=dict(playlist_id=i['id'],
                            channel_id=i['snippet']['channelId'],
                            playlist_name=i['snippet']['title'])
                playlist.append(data_4)
                
            next_page_token=response_playlist.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return playlist

# streamlit-Application Details
im = Image.open(r"D:\Projects\CAPSTONE-Project_1-ML_YouTube Data Harvesting and Warehousing using SQL and Streamlit\YouTube-Logo.png")

st.set_page_config(
    page_title="YouTube Data Harvesting and Warehouse",
    page_icon=im
)

with st.sidebar:
    web = option_menu(
        menu_title="YouTube Data",
        options=["HOME", "DATA COLLECTION", "MIGRATE TO SQL", "DATA ANALYSIS AND VISUALIZATION"],
        icons=["house", "upload", "database", "bar-chart"],  
        menu_icon="cast",  
        default_index=0  
    )

if web == "HOME":
    st.title(":red[You]Tube :green[Data Harvesting and Warehousing using SQL and Streamlit]")
    
    st.markdown("""
        ### :red[Domain:]
        **Social Media**

        ### :red[Overview:]
        Build a simple dashboard or UI using Streamlit and retrieve YouTube channel data using the YouTube API. 
        Store the data in an SQL database (warehousing), enable SQL queries, and finally display the data in Streamlit.

        ### :red[Skill-take:]
        - Python scripting
        - Data Collection
        - API integration
        - Data Management using SQL
        - Streamlit

        ### :red[Developed By:]  
        **Rekha B**
    """)

if web == "DATA COLLECTION":
    st.markdown("### :blue[Data Collection]")
    C = st.text_input("Enter the Channel ID")
    if st.button("Submit"):
        st.success("Channel ID Submitted Successfully")
        with st.spinner('Loading...'):
            time.sleep(5)
    if C:
        # Check if Channel ID is already in the database
        conn = mysql.connector.connect(
             host="localhost",
             user="root",
             password="Mahasri@123",
             database="youtube"
        )
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM channel WHERE channel_id = %s", (C,))
        if my_cursor.fetchone():
            st.error(f"Channel ID {C} is already available")
        else:
            # Collect data and display output
            channel_s = get_channal_info(channel_id=C)
            video_s = get_video_info(Video_ids=get_video_id(channel_id=C))
            playlist_s = get_playlist_info(channel_id=C)
            comments_s = get_comment_info(Video_ids=get_video_id(channel_id=C))
    
            st.markdown("#### Channel Data")
            st.dataframe(channel_s)
            st.markdown("#### Video Data")
            st.dataframe(video_s)
            st.markdown("#### Comments Data")
            st.dataframe(comments_s)
            st.markdown("#### Playlist Data")
            st.dataframe(playlist_s)

# SQL Migration page settings
if web == "MIGRATE TO SQL":
    st.markdown("### :blue[Migrate Data to SQL]")
    
    C = st.text_input("Enter the Channel ID")

    if st.button("Migrate to SQL"):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Mahasri@123"
            )
            if conn.is_connected():
                st.write("Connected to MySQL server")

            my_cursor = conn.cursor()
            my_cursor.execute("CREATE DATABASE IF NOT EXISTS youtube")
            my_cursor.execute("USE youtube")

            my_cursor.execute("SELECT * FROM channel WHERE channel_id = %s", (C,))
            if my_cursor.fetchone():
                st.error(f"Channel ID {C} already exists in the database")
            else:
                # Collect data and migrate to SQL
                channel_s = get_channal_info(channel_id=C)
                video_s = get_video_info(Video_ids=get_video_id(channel_id=C))
                playlist_s = get_playlist_info(channel_id=C)
                comments_s = get_comment_info(Video_ids=get_video_id(channel_id=C))

            create_table_queries = [
                '''CREATE TABLE IF NOT EXISTS channel (
                    channel_name VARCHAR(225),
                    channel_id VARCHAR(225) PRIMARY KEY,
                    subscribers BIGINT,
                    viewscount INT,
                    description TEXT,
                    playlist_id VARCHAR(225)
                )''',
                '''CREATE TABLE IF NOT EXISTS videos (
                    Video_id VARCHAR(225) PRIMARY KEY,
                    video_name VARCHAR(225),
                    channel_name VARCHAR (225),
                    video_description TEXT,
                    PublishedAt TIMESTAMP,
                    view_count BIGINT,
                    like_count BIGINT,
                    Favorite_count INT,
                    comment_count  INT,
                    duration TIME,
                    Thumbnail TEXT,
                    caption_status TEXT
                )''',
                '''CREATE TABLE IF NOT EXISTS playlist (
                    playlist_id VARCHAR(225),
                    channel_id VARCHAR(225),
                    playlist_name VARCHAR(225)
                )''',
                '''CREATE TABLE IF NOT EXISTS comments (
                    comment_id VARCHAR(225),
                    comment_text TEXT,
                    comment_author VARCHAR(225),
                    comment_publishedat TIMESTAMP
                )'''
            ]

            for query in create_table_queries:
                my_cursor.execute(query)

            # Fetch and transform data
            df_channel = pd.DataFrame(get_channal_info(channel_id=C))
            df_video = pd.DataFrame(get_video_info(Video_ids=get_video_id(channel_id=C)))
            df_playlist = pd.DataFrame(get_playlist_info(channel_id=C))
            df_comments = pd.DataFrame(get_comment_info(Video_ids=get_video_id(channel_id=C)))

            # Batch insert queries
            insert_queries = {
                "channel": '''INSERT IGNORE INTO channel 
                              (channel_name, channel_id, subscribers, viewscount, description, playlist_id)
                              VALUES (%s, %s, %s, %s, %s, %s)''',
                "playlist": '''INSERT IGNORE INTO playlist 
                               (playlist_id, channel_id, playlist_name)
                               VALUES (%s, %s, %s)''',
                "comments": '''INSERT IGNORE INTO comments 
                               (comment_id, comment_text, comment_author, comment_publishedat)
                               VALUES (%s, %s, %s, %s)''',
                "videos": '''INSERT IGNORE INTO videos 
                             (Video_id, video_name, channel_name, video_description, PublishedAt, view_count, like_count,
                              Favorite_count, comment_count, duration, Thumbnail, caption_status)
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            }

            def batch_insert(df, query):
                data_to_insert = [tuple(row) for row in df.to_numpy()]
                my_cursor.executemany(query, data_to_insert)

            batch_insert(df_channel, insert_queries["channel"])
            batch_insert(df_playlist, insert_queries["playlist"])
            batch_insert(df_comments, insert_queries["comments"])
            batch_insert(df_video, insert_queries["videos"])
            conn.commit()
            st.success("Data Migrated Successfully to SQL")

        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                my_cursor.close()
                conn.close()

#Query and Visualization

if web == "DATA ANALYSIS AND VISUALIZATION":
    st.markdown("### :blue[SELECT THE QUESTIONS TO GET INSIGHTS]")
    
    options = st.selectbox(
        "Select an option",
        (
            "1. What are the names of all the videos and their corresponding channels?",
            "2. Which channels have the most number of videos, and how many videos do they have?",
            "3. What are the top 10 most viewed videos and their respective channels?",
            "4. How many comments were made on each video, and what are their corresponding video names?",
            "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
            "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
            "7. What is the total number of views for each channel, and what are their corresponding channel names?",
            "8. What are the names of all the channels that have published videos in the year 2022?",
            "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
            "10. Which videos have the highest number of comments, and what are their corresponding channel names?"
        )
    )

    # 1st Query: Video names and corresponding channels
    if options == "1. What are the names of all the videos and their corresponding channels?":
        if st.button("SUBMIT"):
            conn = mysql.connector.connect(host="localhost", user="root", password="Mahasri@123", database="youtube")
            my_cursor = conn.cursor()
            my_cursor.execute('''SELECT video_name, channel_name FROM videos ORDER BY channel_name''')
            out = my_cursor.fetchall()
            que_1 = pd.DataFrame(out, columns=["Video Name", "Channel Name"])
            st.markdown("### **Video Names and Corresponding Channels**")
            st.write(que_1)

    # 2nd Query: Channels with the most number of videos
    if options == "2. Which channels have the most number of videos, and how many videos do they have?":
        if st.button("SUBMIT"):
            conn = mysql.connector.connect(host="localhost", user="root", password="Mahasri@123", database="youtube")
            my_cursor = conn.cursor()
            my_cursor.execute('''SELECT COUNT(DISTINCT channel_name) FROM videos''')
            total_channels = my_cursor.fetchone()[0]
            my_cursor.execute('''SELECT channel_name, COUNT(Video_id) AS video_count FROM videos
                                GROUP BY channel_name ORDER BY video_count DESC''')
            out = my_cursor.fetchall()
            que_2 = pd.DataFrame(out, columns=["Channel Name", "Video Count"])
            st.markdown("### **Channels with the Most Number of Videos**")
            st.write(que_2)

            #Visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=que_2, x="Channel Name", y="Video Count", ax=ax, palette="viridis")
            ax.set_title("Video Count by Channel", fontsize=14, color='navy', weight='bold')
            ax.set_xlabel("Channel", fontsize=12, color='darkred', weight='bold')
            ax.set_ylabel("Video Count", fontsize=12, color='darkgreen', weight='bold')
            ax.tick_params(axis='x', rotation=45, labelsize=10)  
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig)
 
    # 3rd Query: Top 10 most viewed videos
    if options == "3. What are the top 10 most viewed videos and their respective channels?":
        if st.button("SUBMIT"):
            conn = mysql.connector.connect(host="localhost", user="root", password="Mahasri@123", database="youtube")
            my_cursor = conn.cursor()
            my_cursor.execute('''SELECT channel_name, video_name, view_count FROM videos
                                 ORDER BY view_count DESC LIMIT 10''')
            out = my_cursor.fetchall()
            que_3 = pd.DataFrame(out, columns=["Channel Name", "Video Name", "View Count"])
            st.markdown("### **Top 10 Most Viewed Videos and Their Channels**")
            st.write(que_3)

            # Visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=que_3, x="Video Name", y="View Count", hue="Channel Name", ax=ax, palette="coolwarm")
            ax.set_title("Top 10 Most Viewed Videos", fontsize=14, color='navy', weight='bold')
            ax.set_xlabel("Video Name", fontsize=12, color='darkred', weight='bold')
            ax.set_ylabel("View Count", fontsize=12, color='darkgreen', weight='bold')
            ax.tick_params(axis='x', rotation=45, labelsize=10)  
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig)

    # 4th Query: Comments per video
    if options == "4. How many comments were made on each video, and what are their corresponding video names?":
        if st.button("SUBMIT"):
            conn = mysql.connector.connect(host="localhost", user="root", password="Mahasri@123", database="youtube")
            my_cursor = conn.cursor()
            my_cursor.execute('''SELECT video_name, comment_count FROM videos
                                 ORDER BY comment_count DESC LIMIT 20''')
            out = my_cursor.fetchall()
            que_4 = pd.DataFrame(out, columns=["Video Name", "Total Comments"])
            st.markdown("### **Total Comments on Each Video**")
            st.write(que_4)

            #Visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=que_4, x="Video Name", y="Total Comments", ax=ax, palette="coolwarm")
            ax.set_title("Top 20 Most Videos Total Comments", fontsize=14, color='navy', weight='bold')
            ax.set_xlabel("Video Name", fontsize=12, color='darkred', weight='bold')
            ax.set_ylabel("Total Comments", fontsize=12, color='darkgreen', weight='bold')
            ax.tick_params(axis='x', rotation=45, labelsize=10)  
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            st.pyplot(fig)

    # 5th Query: Highest number of likes
    if options == "5. Which videos have the highest number of likes, and what are their corresponding channel names?":
        if st.button("SUBMIT"):
            conn = mysql.connector.connect(host="localhost", user="root", password="Mahasri@123", database="youtube")
            my_cursor = conn.cursor()
            my_cursor.execute('''SELECT video_name, like_count, channel_name FROM videos
                                 ORDER BY like_count DESC LIMIT 10''')
            out = my_cursor.fetchall()
            que_5 = pd.DataFrame(out, columns=["Video Name", "Like Count", "Channel Name"])
            st.markdown("### **Videos with the Highest Number of Likes**")
            st.write(que_5)

            # Visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=que_5, x="Video Name", y="Like Count", hue="Channel Name", ax=ax, palette="magma")
            ax.set_title("Top 10 Videos by Like Count", fontsize=14, color='navy', weight='bold')
            ax.set_xlabel("Video Name", fontsize=12, color='darkred', weight='bold')
            ax.set_ylabel("Like Count", fontsize=12, color='darkgreen', weight='bold')
            ax.tick_params(axis='x', rotation=45, labelsize=10)  
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')  
            st.pyplot(fig)

    
    # 6th Query: Total likes and dislikes per video
    if options == "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
        if st.button("SUBMIT"):
            conn = mysql.connector.connect(host="localhost", user="root", password="Mahasri@123", database="youtube")
            my_cursor = conn.cursor()
            my_cursor.execute('''SELECT video_name, like_count FROM videos ORDER BY like_count DESC LIMIT 10''')
            out = my_cursor.fetchall()
            que_6 = pd.DataFrame(out, columns=["Video Name", "Like Count"])
            st.markdown("### **Total Number of Likes for Each Video**")
            st.write(que_6)
    
            # Visualization
            fig, ax = plt.subplots(figsize=(12, 8)) 
            sns.barplot(data=que_6, x="Video Name", y="Like Count", palette="rocket", ax=ax)
            ax.set_title("Top 10 Videos by Like Count", fontsize=14, color='navy', weight='bold')
            ax.set_xlabel("Video Name", fontsize=12, color='darkred', weight='bold')
            ax.set_ylabel("Like Count", fontsize=12, color='darkgreen', weight='bold')
            ax.tick_params(axis='x', rotation=45, labelsize=10)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right') 
            st.pyplot(fig)
    

    # 7th Query: Total views for each channel
    if options == "7. What is the total number of views for each channel, and what are their corresponding channel names?":
        if st.button("SUBMIT"):
            conn = mysql.connector.connect(host="localhost", user="root", password="Mahasri@123", database="youtube")
            my_cursor = conn.cursor()
            my_cursor.execute('''SELECT channel_name, viewscount AS total_views FROM channel ORDER BY viewscount DESC''')
            out = my_cursor.fetchall()
            que_7 = pd.DataFrame(out, columns=["Channel Name", "Total Views"])
            st.markdown("### **Total Views for Each Channel**")
            st.write(que_7)

            # Visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=que_7, x="Channel Name", y="Total Views", palette="crest", ax=ax)
            ax.set_title("Total Views by Channel", fontsize=14, color='navy', weight='bold')
            ax.set_xlabel("Channel Name", fontsize=12, color='darkred', weight='bold')
            ax.set_ylabel("Total Views", fontsize=12, color='darkgreen', weight='bold')
            ax.tick_params(axis='x', rotation=45, labelsize=10) 
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')  
            st.pyplot(fig)


    # 8th Query: Channels that published videos in 2022
    if options == "8. What are the names of all the channels that have published videos in the year 2022?":
        if st.button("SUBMIT"):
            conn = mysql.connector.connect(host="localhost", user="root", password="Mahasri@123", database="youtube")
            my_cursor = conn.cursor()
            my_cursor.execute('''SELECT channel_name, video_name, PublishedAt FROM videos WHERE YEAR(PublishedAt) = 2022''')
            out = my_cursor.fetchall()
            que_8 = pd.DataFrame(out, columns=["Channel Name", "Video Name", "Published At"])
            st.markdown("### **Channels that Published Videos in 2022**")
            st.write(que_8)

            # Visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=que_8, x="Published At", kde=False, color="purple", ax=ax)
            ax.set_title("Video Publications in 2022", fontsize=14, color='navy', weight='bold')
            ax.set_xlabel("Publication Date", fontsize=12, color='darkred', weight='bold')
            ax.set_ylabel("count", fontsize=12, color='darkgreen', weight='bold')
            ax.tick_params(axis='x', rotation=45, labelsize=10) 
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')  
            st.pyplot(fig)


    # 9th Query: Average duration of videos per channel
    if options == "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?":
        if st.button("SUBMIT"):
            conn = mysql.connector.connect(host="localhost", user="root", password="Mahasri@123", database="youtube")
            my_cursor = conn.cursor()
            my_cursor.execute('''SELECT channel_name, AVG(duration)/60 AS avg_duration FROM videos 
                                 GROUP BY channel_name ORDER BY avg_duration DESC''')
            out = my_cursor.fetchall()
            que_9 = pd.DataFrame(out, columns=["Channel Name", "Average Duration (minutes)"])
            st.markdown("### **Average Duration of Videos per Channel**")
            st.write(que_9)

            # Visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=que_9, x="Channel Name", y="Average Duration (minutes)", palette="coolwarm", ax=ax)
            ax.set_title("Average Duration of Videos by Channel", fontsize=14, color='navy', weight='bold')
            ax.set_xlabel("Channel Name", fontsize=12, color='darkred', weight='bold')
            ax.set_ylabel("Average Duration (minutes)", fontsize=12, color='darkgreen', weight='bold')
            ax.tick_params(axis='x', rotation=45, labelsize=10) 
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right') 
            st.pyplot(fig)


    # 10th Query: Videos with the highest number of comments
    if options == "10. Which videos have the highest number of comments, and what are their corresponding channel names?":
        if st.button("SUBMIT"):
            conn = mysql.connector.connect(host="localhost", user="root", password="Mahasri@123", database="youtube")
            my_cursor = conn.cursor()
            my_cursor.execute('''SELECT video_name, comment_count, channel_name FROM videos
                                 ORDER BY comment_count DESC LIMIT 10''')
            out = my_cursor.fetchall()
            que_10 = pd.DataFrame(out, columns=["Video Name", "Comment Count", "Channel Name"])
            st.markdown("### **Top 10 Videos with the Highest Number of Comments**")
            st.write(que_10)

            # Visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=que_10, x="Video Name", y="Comment Count", palette="light:#5A9", ax=ax)
            ax.set_title("Top 10 Videos by Comment Count", fontsize=14, color='navy', weight='bold')
            ax.set_xlabel("Video Name", fontsize=12, color='darkred', weight='bold')
            ax.set_ylabel("Comment Count", fontsize=12, color='darkgreen', weight='bold')
            ax.tick_params(axis='x', rotation=45, labelsize=10)  
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')  
            st.pyplot(fig)


                

    

                