import streamlit as st
import yt_dlp
import os
import uuid
import re


def progress_hook(d):
    """Hook to update Streamlit progress bar in real-time."""
    if d['status'] == 'downloading':
        # Safely extract and parse the percentage
        p = d.get('_percent_str', '0%').replace('%', '').strip()
        p = re.sub(r'\x1b\[[0-9;]*m', '', p)  # Remove terminal color codes
        try:
            percent = max(0.0, min(1.0, float(p) / 100.0))
            if 'progress_bar' in st.session_state:
                st.session_state['progress_bar'].progress(percent)
            if 'status_text' in st.session_state:
                speed = d.get('_speed_str', 'N/A')
                st.session_state['status_text'].text(f"Downloading... {p}% (Speed: {speed})")
        except ValueError:
            pass
    elif d['status'] == 'finished':
        if 'progress_bar' in st.session_state:
            st.session_state['progress_bar'].progress(1.0)
        if 'status_text' in st.session_state:
            st.session_state['status_text'].text("Merging video and audio streams... (This may take a moment)")


def download_youtube_video(url, format_choice="best"):
    output_dir = "temp_downloads"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    unique_id = uuid.uuid4().hex[:6]

    # Map the UI choices to yt-dlp format strings
    format_map = {
        "Best Quality (Video + Audio)": "bestvideo+bestaudio/best",
        "Standard Quality (720p)": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "Audio Only (MP3)": "bestaudio/best"
    }

    ydl_opts = {
        'format': format_map.get(format_choice, "best"),
        'outtmpl': f'{output_dir}/%(title)s_{unique_id}.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'progress_hooks': [progress_hook],
    }

    # If the user selected MP3, add an FFmpeg post-processor
    if format_choice == "Audio Only (MP3)":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)

            # Predict the exact output file path depending on post-processors
            if format_choice == "Audio Only (MP3)":
                final_file_path = os.path.splitext(ydl.prepare_filename(info_dict))[0] + ".mp3"
            else:
                ext = ydl.prepare_filename(info_dict)
                base = os.path.splitext(ext)[0]
                if not os.path.exists(ext):
                    # Check if FFmpeg altered the container extension during merge
                    for possible_ext in ['.mp4', '.mkv', '.webm']:
                        if os.path.exists(base + possible_ext):
                            final_file_path = base + possible_ext
                            break
                    else:
                        final_file_path = ext
                else:
                    final_file_path = ext

            return final_file_path, info_dict.get('title', 'YouTube Video')

    except Exception as e:
        st.error(f"Error during download: {e}")
        return None, None