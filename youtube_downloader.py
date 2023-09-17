import streamlit as st
from pytube import Playlist, YouTube
import tempfile

def get_video_stream(video_url):
    video = YouTube(video_url)
    stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    return stream

def download_playlist_videos(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        st.write('Number of videos in playlist:', len(playlist.video_urls))

        for video_url in playlist.video_urls:
            video_stream = get_video_stream(video_url)
            with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
                video_stream.stream_to_buffer(tmpfile)
                tmpfile.flush()
                st.download_button(label=f"Download {video_stream.title}", data=tmpfile.name, file_name=f"{video_stream.title}.mp4")

    except Exception as e:
        st.error(f"An error occurred: {e}")

def get_audio_stream(music_url):
    music = YouTube(music_url)
    stream = music.streams.filter(only_audio=True, file_extension='mp4').first()
    return stream

st.title("YouTube Downloader")

url = st.text_input("Enter the YouTube URL:", "")

options = ["Single Video", "Playlist", "Music (audio only)"]
choice = st.radio("What type of content is the URL?", options)

if st.button("Download"):
    if url:
        if choice == "Single Video":
            video_stream = get_video_stream(url)
            with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
                video_stream.stream_to_buffer(tmpfile)
                tmpfile.flush()
                st.download_button(label=f"Download {video_stream.title}", data=tmpfile.name, file_name=f"{video_stream.title}.mp4")

        elif choice == "Playlist":
            download_playlist_videos(url)

        elif choice == "Music (audio only)":
            audio_stream = get_audio_stream(url)
            with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
                audio_stream.stream_to_buffer(tmpfile)
                tmpfile.flush()
                st.download_button(label=f"Download audio of {audio_stream.title}", data=tmpfile.name, file_name=f"{audio_stream.title}.mp4")

    else:
        st.warning("Please enter a valid URL.")