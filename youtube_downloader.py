import streamlit as st
from pytube import Playlist, YouTube

def download_single_video(video_url):
    try:
        video = YouTube(video_url)
        video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
        st.success(f"Downloaded {video.title}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def download_playlist_videos(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        st.write('Number of videos in playlist:', len(playlist.video_urls))

        for video in playlist.videos:
            video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
            st.write(f"Downloaded {video.title}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def download_music_audio(music_url):
    try:
        music = YouTube(music_url)
        music.streams.filter(only_audio=True, file_extension='mp4').first().download()
        st.success(f"Downloaded audio of {music.title}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.title("YouTube Downloader")

url = st.text_input("Enter the YouTube URL:", "")

options = ["Single Video", "Playlist", "Music (audio only)"]
choice = st.radio("What type of content is the URL?", options)

if st.button("Download"):
    if url:
        if choice == "Single Video":
            download_single_video(url)
        elif choice == "Playlist":
            download_playlist_videos(url)
        elif choice == "Music (audio only)":
            download_music_audio(url)
    else:
        st.warning("Please enter a valid URL.")
