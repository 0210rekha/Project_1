
#importing the necessary libraries
import pandas as pd
import mysql.connector as sql
import mysql.connector
import pymongo
from googleapiclient.discovery import build

# BUILDING CONNECTION WITH YOUTUBE API
api_key = "AIzaSyAr2S7hQ6hzH7gh_nDyA6vyTF80xJAoHs4"
youtube = build('youtube','v3',developerKey=api_key)

# FUNCTION TO GET CHANNEL DETAILS
def get_channel_details(channel_id):
    ch_data = []
    response = youtube.channels().list(part = 'snippet,contentDetails,statistics',
                                     id= channel_id).execute()

    for i in range(len(response['items'])):
        data = dict(Channel_id = channel_id[i],
                    Channel_name = response['items'][i]['snippet']['title'],
                    Playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                    Subscribers = response['items'][i]['statistics']['subscriberCount'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_videos = response['items'][i]['statistics']['videoCount'],
                    Description = response['items'][i]['snippet']['description'],
                    Country = response['items'][i]['snippet'].get('country')
                    )
        ch_data.append(data)
    return ch_data


# FUNCTION TO GET VIDEO IDS
def get_channel_videos(channel_id):
    video_ids = []
    # get Uploads playlist id
    res = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None
    
    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id, 
                                           part='snippet', 
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        
        for i in range(len(res['items'])):
            video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = res.get('nextPageToken')
        
        if next_page_token is None:
            break
    return video_ids


# FUNCTION TO GET VIDEO DETAILS
def get_video_details(v_ids):
    video_stats = []
    
    for i in range(0, len(v_ids), 50):
        response = youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=','.join(v_ids[i:i+50])).execute()
        for video in response['items']:
            # Safe access for 'duration' and other potentially missing fields
            video_details = dict(
                Channel_name = video['snippet']['channelTitle'],
                Channel_id = video['snippet']['channelId'],
                Video_id = video['id'],
                Title = video['snippet']['title'],
                Tags = video['snippet'].get('tags'),
                Thumbnail = video['snippet']['thumbnails']['default']['url'],
                Description = video['snippet']['description'],
                Published_date = video['snippet']['publishedAt'],
                Duration = video['contentDetails'].get('duration', 'N/A'),  # Use .get() to handle missing 'duration'
                Views = video['statistics'].get('viewCount', 0),  # Safe default to 0 if missing
                Likes = video['statistics'].get('likeCount', 0),
                Comments = video['statistics'].get('commentCount', 0),
                Favorite_count = video['statistics'].get('favoriteCount', 0),
                Definition = video['contentDetails'].get('definition', 'N/A'),
                Caption_status = video['contentDetails'].get('caption', 'N/A')
            )
            video_stats.append(video_details)
    return video_stats


# FUNCTION TO GET COMMENT DETAILS
def get_comments_details(v_id):
    comment_data = []
    try:
        next_page_token = None
        while True:
            response = youtube.commentThreads().list(part="snippet,replies",
                                                    videoId=v_id,
                                                    maxResults=100,
                                                    pageToken=next_page_token).execute()
            for cmt in response['items']:
                data = dict(Comment_id = cmt['id'],
                            Video_id = cmt['snippet']['videoId'],
                            Comment_text = cmt['snippet']['topLevelComment']['snippet']['textDisplay'],
                            Comment_author = cmt['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            Comment_posted_date = cmt['snippet']['topLevelComment']['snippet']['publishedAt'],
                            Like_count = cmt['snippet']['topLevelComment']['snippet']['likeCount'],
                            Reply_count = cmt['snippet']['totalReplyCount']
                           )
                comment_data.append(data)
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return comment_data

#FUNCTION TO GET PLAYLIST DETAILS

def get_playlist_details(channel_id):

    All_data=[]

    next_page_token=None
    while True:
        request=youtube.playlists().list(
            part='snippet, contentDetails',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response=request.execute()

        for item in response['items']:
            data=dict(
                Playlist_Id=item['id'],
                Title=item['snippet']['title'],
                Channel_id=item['snippet']['channelId'],
                Channel_Name=item['snippet']['channelTitle'],
                PublishedAt=item['snippet']['publishedAt'],
                Video_Count=item['contentDetails']['itemCount']
            )
            All_data.append(data)
        next_page_token=response.get('nextPageToken')
        if next_page_token is None:
            break
    return All_data 

playlist_details=get_playlist_details('UCKhxMazNAuU-SAgz4dtJLFw')
channel_ids = get_channel_details('UCKhxMazNAuU-SAgz4dtJLFw')
Video_Ids=get_channel_videos('UCKhxMazNAuU-SAgz4dtJLFw')

#####################################################################################################

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
#Creating database
db  = client["youtube_data"]

import pymongo

# Connect to MongoDB (replace with your connection string if using Atlas)
client = pymongo.MongoClient("mongodb://localhost:27017/") 

# Create database and collections
db = client['youtube_db'] # Create database
channel_collection = db['channels'] # Create collection for channels
video_collection = db['videos'] # Create collection for videos
comment_collection = db['comments'] # Create collection for comments
playlist_collection = db['playlists'] # Create collection for playlists

# Function to insert channel details into MongoDB
def insert_channel_details(channel_details):
    channel_collection.insert_many(channel_details)
    print(f"Inserted {len(channel_details)} channel details into MongoDB.")

# Function to insert video details into MongoDB
def insert_video_details(video_details):
    video_collection.insert_many(video_details)
    print(f"Inserted {len(video_details)} video details into MongoDB.")

# Function to insert comments details into MongoDB
def insert_comment_details(comment_details):
    comment_collection.insert_many(comment_details)
    print(f"Inserted {len(comment_details)} comments into MongoDB.")

# Function to insert playlist details into MongoDB
def insert_playlist_details(playlist_details):
    playlist_collection.insert_many(playlist_details)
    print(f"Inserted {len(playlist_details)} playlists into MongoDB.")

# Get the details
channel_details = get_channel_details('UCKhxMazNAuU-SAgz4dtJLFw')
playlist_details = get_playlist_details('UCKhxMazNAuU-SAgz4dtJLFw')
video_ids = get_channel_videos('UCKhxMazNAuU-SAgz4dtJLFw')   
video_details = get_video_details(video_ids)

# Insert data into MongoDB
insert_channel_details(channel_details)
insert_playlist_details(playlist_details)
insert_video_details(video_details)

# Optionally, you can also fetch comments for each video and insert them
for video_id in video_ids:
    comments = get_comments_details(video_id)
    if comments:
        insert_comment_details(comments)


#####################################################################################################

import mysql.connector
from datetime import datetime

# Define the ISO to MySQL datetime conversion function
def convert_iso_to_mysql_datetime(iso_datetime):
    try:
        # Parse the ISO 8601 date string and convert to MySQL DATETIME format
        return datetime.strptime(iso_datetime, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        print(f"Date conversion error: {e}, input date: {iso_datetime}")
        return None

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mahasri@123",
    database="youtube_data_new"
)

cursor = mydb.cursor()

# Drop existing tables if they exist
cursor.execute("DROP TABLE IF EXISTS comments;")
cursor.execute("DROP TABLE IF EXISTS videos;")
cursor.execute("DROP TABLE IF EXISTS playlists;")
cursor.execute("DROP TABLE IF EXISTS channel_details;")

# Create tables
create_channel = """
CREATE TABLE channel_details (
    Channel_id VARCHAR(255) PRIMARY KEY,
    Channel_name VARCHAR(255),
    Playlist_id VARCHAR(255),
    Subscribers INT,
    Views INT,
    Total_videos INT,
    Description TEXT,
    Channel_Status VARCHAR(255)
)
"""
cursor.execute(create_channel)

create_playlist = """
CREATE TABLE playlists (
    Playlist_id VARCHAR(255) PRIMARY KEY,
    Channel_id VARCHAR(255),
    Playlist_name VARCHAR(255),
    FOREIGN KEY (Channel_id) REFERENCES channel_details(Channel_id)
)
"""
cursor.execute(create_playlist)

create_videos = """
CREATE TABLE videos (
    Video_id VARCHAR(255) PRIMARY KEY,
    Playlist_id VARCHAR(255),
    Video_name VARCHAR(255),
    Thumbnail VARCHAR(255),
    Description TEXT,
    Published_date DATETIME,
    Duration VARCHAR(50),
    Views BIGINT,
    Likes BIGINT,
    Comments BIGINT,
    Favorite_count BIGINT,
    Definition VARCHAR(50),
    Caption_status VARCHAR(50),
    FOREIGN KEY (Playlist_id) REFERENCES playlists(Playlist_id)
)
"""
cursor.execute(create_videos)

create_comments = """
CREATE TABLE comments (
    Comment_id VARCHAR(255) PRIMARY KEY,
    Video_id VARCHAR(255),
    Comment_text TEXT,
    Comment_author VARCHAR(255),
    Comment_posted_date DATETIME,
    FOREIGN KEY (Video_id) REFERENCES videos(Video_id)
)
"""
cursor.execute(create_comments)

# Commit the changes to the database
mydb.commit()

print("Tables created successfully.")

# Insert functions
# Define a global variable
existing_channel_ids = set()

def fetch_existing_channel_ids():
    global existing_channel_ids
    cursor.execute("SELECT Channel_id FROM channel_details")
    existing_channel_ids = {row[0] for row in cursor.fetchall()}
    print(f"Fetched Existing Channel IDs: {existing_channel_ids}")

# Call this function after inserting channel details and committing
def insert_channel_details_mysql(channel_details):
    sql = """
    INSERT INTO channel_details (Channel_id, Channel_name, Playlist_id, Subscribers, Views, Total_videos, Description, Channel_Status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE Channel_name=VALUES(Channel_name), Subscribers=VALUES(Subscribers), Views=VALUES(Views),
                            Total_videos=VALUES(Total_videos), Description=VALUES(Description), Channel_Status=VALUES(Channel_Status)
    """
    for ch in channel_details:
        try:
            val = (
                ch['Channel_id'], 
                ch['Channel_name'], 
                ch['Playlist_id'], 
                ch['Subscribers'], 
                ch['Views'], 
                ch['Total_videos'], 
                ch['Description'], 
                ch.get('Channel_Status', 'Unknown')
            )
            cursor.execute(sql, val)
        except KeyError as e:
            print(f"Error inserting channel: {e}, data: {ch}")
    
    mydb.commit()
    print("Channel details inserted successfully.")
    
    # Fetch existing channel IDs after committing
    fetch_existing_channel_ids()

def insert_playlist_details_mysql(playlist_details):
    sql = """
    INSERT INTO playlists (Playlist_id, Channel_id, Playlist_name)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE Playlist_name=VALUES(Playlist_name)
    """
    
    skipped_playlists = 0
    
    for playlist in playlist_details:
        try:
            playlist_id = playlist.get('Playlist_Id')
            channel_id = playlist.get('Channel_id')
            playlist_name = playlist.get('Title')
            
            print(f"Attempting to insert Playlist ID: {playlist_id}, Channel ID: {channel_id}, Playlist Name: {playlist_name}")
            
            if channel_id not in existing_channel_ids:
                print(f"Error inserting playlist: Channel_id {channel_id} does not exist, data: {playlist}")
                skipped_playlists += 1
                continue
            
            val = (playlist_id, channel_id, playlist_name)
            cursor.execute(sql, val)
        except KeyError as e:
            print(f"Error inserting playlist: Missing key {e}, data: {playlist}")
        except mysql.connector.Error as err:
            print(f"MySQL error: {err}, data: {playlist}")
        except Exception as e:
            print(f"Unexpected error: {e}, data: {playlist}")
    
    mydb.commit()
    print(f"Inserted {len(playlist_details) - skipped_playlists} playlist records into MySQL.")
    if skipped_playlists > 0:
        print(f"Skipped {skipped_playlists} playlists due to missing channel records.")


def insert_video_details_mysql(video_details):
    sql = """
    INSERT INTO videos (Video_id, Playlist_id, Video_name, Thumbnail, Description, Published_date, Duration, Views, Likes, Comments, Favorite_count, Definition, Caption_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE Video_name=VALUES(Video_name), Views=VALUES(Views), Likes=VALUES(Likes), Comments=VALUES(Comments)
    """
    for video in video_details:
        try:
            published_date = convert_iso_to_mysql_datetime(video.get('Published_date'))
            val = (
                video['Video_id'], 
                video.get('Playlist_id'), 
                video.get('Video_name'),
                video.get('Thumbnail'),
                video.get('Description'),
                published_date,
                video.get('Duration'),
                video.get('Views'),
                video.get('Likes'),
                video.get('Comments'),
                video.get('Favorite_count'),
                video.get('Definition'),
                video.get('Caption_status')
            )
            cursor.execute(sql, val)
        except KeyError as e:
            print(f"Error inserting video: Missing key {e}, data: {video}")
    
    mydb.commit()
    print(f"Inserted {len(video_details)} video records into MySQL.")


def insert_comment_details_mysql(comment_details):
    sql = """
    INSERT INTO comments (Comment_id, Video_id, Comment_text, Comment_author, Comment_posted_date)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE Comment_text=VALUES(Comment_text)
    """
    
    cursor.execute("SELECT Video_id FROM videos")
    existing_video_ids = {row[0] for row in cursor.fetchall()}
    
    skipped_comments = 0
    
    for comment in comment_details:
        try:
            posted_date = convert_iso_to_mysql_datetime(comment['Comment_posted_date'])
            if posted_date is None:
                skipped_comments += 1
                continue
            
            video_id = comment['Video_id']
            if video_id not in existing_video_ids:
                print(f"Error inserting comment: Video_id {video_id} does not exist, data: {comment}")
                skipped_comments += 1
                continue
            
            val = (
                comment['Comment_id'], 
                video_id, 
                comment['Comment_text'], 
                comment['Comment_author'], 
                posted_date
            )
            cursor.execute(sql, val)
        except KeyError as e:
            print(f"Error inserting comment: Missing key {e}, data: {comment}")
        except Exception as e:
            print(f"Unexpected error: {e}, data: {comment}")
    
    mydb.commit()
    print(f"Inserted {len(comment_details) - skipped_comments} comment records into MySQL.")
    if skipped_comments > 0:
        print(f"Skipped {skipped_comments} comments due to missing video records.")

# Assuming playlist_details, channel_details, video_details, and video_ids are defined
# Insert data into MySQL
insert_playlist_details_mysql(playlist_details)
insert_channel_details_mysql(channel_details)
insert_video_details_mysql(video_details)

# Optionally insert comments for each video
for video_id in video_ids:
    comments = get_comments_details(video_id)
    if comments:
        insert_comment_details_mysql(comments)

#####################################################################################################

 