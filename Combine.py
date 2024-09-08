import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define your YouTube API key here
API_KEY = 
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


# Create a YouTube API client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

def search_videos(query):
    try:
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id',
            maxResults=15# Adjust this number as needed
        ).execute()

        video_ids = [item['id']['videoId'] for item in search_response['items']]
        return video_ids
    except HttpError as e:
        print(f"An error occurred: {e}")
        return []
    
def content_filter(video_ids):
    filtered_video_ids = []

    for video_id in video_ids:
        video_response = youtube.videos().list(
            id=video_id,
            part='snippet'
        ).execute()

        # Check if the video title contains the keyword "gaming"
        title = video_response['items'][0]['snippet']['title'].lower()
        if 'gaming' not in title:
            filtered_video_ids.append(video_id)

    return filtered_video_ids

def recommend_videos(video_ids):
    # Content filtering
    filtered_video_ids = content_filter(video_ids)
   # Get more information about each video ID
    return filtered_video_ids



def recommend_button_click():
    query = search_entry.get()
    video_ids = search_videos(query)
    recommended_video_ids = recommend_videos(video_ids)

    recommended_videos.delete(1.0, tk.END)  # Clear previous recommendations
    for video_id in recommended_video_ids:
        recommended_videos.insert(tk.END, f"https://www.youtube.com/watch?v={video_id}\n")


# Create the GUI
root = tk.Tk()
root.title("YouTube Video Recommender")

search_label = tk.Label(root, text="Search for videos:")
search_label.pack()

search_entry = tk.Entry(root)
search_entry.pack()

search_button = tk.Button(root, text="Search", command=recommend_button_click)
search_button.pack()

recommended_label = tk.Label(root, text="Recommended Videos:")
recommended_label.pack()

recommended_videos = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=100)
recommended_videos.pack()

root.mainloop()
