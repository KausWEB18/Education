import tkinter as tk
from tkinter import scrolledtext
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.neighbors import NearestNeighbors

# Define your YouTube API key here
API_KEY = 'AIzaSyA4sLLyGgPGnpxgTOg-VBPf41JVVP-zdSY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# YouTube API client
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

#  tkinter window
root = tk.Tk()
root.title("Video Recommender")

# Text widget for user input
query_label = tk.Label(root, text="Enter your interests:")
query_label.pack()
query_entry = tk.Entry(root, width=40)
query_entry.pack()

# scrolled Text widget for recommended videos
recommended_videos = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
recommended_videos.pack()

def search_videos(query):
    try:
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id,snippet',
            maxResults=10  # number of results
        ).execute()

        video_data = [{'title': item['snippet']['title'], 'description': item['snippet']['description']} for item in search_response['items']]
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        return video_data,video_ids;
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def content_recommendations(video_data, user_query):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([v['description'] for v in video_data])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix) # change 9-6-2023
    tfidf_matrix=linear_kernel(tfidf_vectorizerd(tfidf_matrix))

    query_vector = tfidf_vectorizer.transform([user_query])
    cosine_sim_scores = list(enumerate(cosine_sim[query_vector.nonzero()[0][0]]))
    cosine_sim_scores = sorted(cosine_sim_scores, key=lambda x: x[1], reverse=True)
    cosine_sim_scores = cosine_sim_scores[1:6]  # Exclude the query itself
    video_indices = [i[0] for i in cosine_sim_scores]
    return [video_data[i]['title'] for i in video_indices]

def collaborative_recommendations(video_data, user_query):
    # this part needs to be updated with User preference API to create collaborative system
    return content_recommendations(video_data, user_query)

def recommend_videos():
    user_query = query_entry.get()
    video_data = search_videos(user_query)
    query = search_videos.get()
    video_ids = search_videos(query)
    recommended_video_ids = recommend_videos(video_ids)

    content_recommendations_result = content_recommendations(video_data, user_query)
    collaborative_recommendations_result = collaborative_recommendations(video_data, user_query)

    # Combine content-based and collaborative recommendations
    combined_recommendations = content_recommendations_result + collaborative_recommendations_result
    recommended_videos.delete(1.0, tk.END)  # Clear previous recommendations
    for video_title in combined_recommendations:
        recommended_videos.insert(tk.END, f"{video_title}\n")
    recommended_videos.delete(1.0, tk.END)  # Clear previous recommendations
    for video_id in recommended_video_ids:
        recommended_videos.insert(tk.END, f"https://www.youtube.com/watch?v={video_id}\n")    
      

# button for recommendations
recommend_button = tk.Button(root, text="Recommend Videos", command=recommend_videos)
recommend_button.pack()

root.mainloop()
