import os
import re
import uuid
import json
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
import streamlit as st
import yt_dlp


def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%', '').strip()
        p = re.sub(r'\x1b\[[0-9;]*m', '', p)
        try:
            percent = max(0.0, min(1.0, float(p) / 100.0))
            if 'progress_bar' in st.session_state:
                st.session_state['progress_bar'].progress(percent)
            if 'status_text' in st.session_state:
                speed = d.get('_speed_str', 'N/A')
                st.session_state['status_text'].text(f"Downloading: {p}% (Speed: {speed})")
        except ValueError:
            pass
    elif d['status'] == 'finished':
        if 'progress_bar' in st.session_state:
            st.session_state['progress_bar'].progress(1.0)
        if 'status_text' in st.session_state:
            st.session_state['status_text'].text("Finalizing file processing...")


def convert_spotify_to_ytsearch(spotify_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(spotify_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title').text
        clean_title = title_tag.split('|')[0].replace("song and lyrics by", "").strip()
        return f"ytsearch1:{clean_title} audio"
    except Exception:
        return None


def json_to_netscape(json_data):
    lines = ["# Netscape HTTP Cookie File"]
    for cookie in json_data:
        domain = cookie.get('domain', '')
        include_sub = 'TRUE' if domain.startswith('.') else 'FALSE'
        path = cookie.get('path', '/')
        secure = 'TRUE' if cookie.get('secure') else 'FALSE'
        exp = cookie.get('expirationDate', cookie.get('expiry', 0))
        exp = str(int(exp)) if exp else "0"
        name = cookie.get('name', '')
        value = cookie.get('value', '')
        lines.append(f"{domain}\t{include_sub}\t{path}\t{secure}\t{exp}\t{name}\t{value}")
    return "\n".join(lines)


def header_to_netscape(header_string, url):
    domain = urlparse(url).netloc
    if not domain.startswith('.'):
        domain = '.' + domain
    lines = ["# Netscape HTTP Cookie File"]
    header_string = header_string.replace('Cookie:', '').strip()
    pairs = header_string.split(';')
    for pair in pairs:
        if '=' in pair:
            name, value = pair.strip().split('=', 1)
            lines.append(f"{domain}\tTRUE\t/\tTRUE\t0\t{name}\t{value}")
    return "\n".join(lines)


def process_raw_cookies(raw_data, cookie_format, target_url):
    temp_file = f"temp_cookies_{uuid.uuid4().hex[:6]}.txt"
    try:
        if cookie_format == "JSON":
            try:
                data = json.loads(raw_data)
                netscape_data = json_to_netscape(data)
            except json.JSONDecodeError:
                st.error("Invalid JSON format provided.")
                return None
        elif cookie_format == "Header String":
            netscape_data = header_to_netscape(raw_data, target_url)
        else:
            netscape_data = raw_data

        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(netscape_data)
        return temp_file
    except Exception as e:
        st.error(f"Error processing cookies: {e}")
        return None


def get_media_info(url, platform="Generic", cookie_path=None, browser=None):
    if platform == "Spotify":
        search_query = convert_spotify_to_ytsearch(url)
        if not search_query:
            return None
        url = search_query

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'skip_download': True
    }

    if browser and browser != "None":
        ydl_opts['cookiesfrombrowser'] = (browser.lower(),)
    elif cookie_path and os.path.exists(cookie_path):
        ydl_opts['cookiefile'] = cookie_path
    elif os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = 'cookies.txt'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                info = info['entries'][0]

            return {
                'title': info.get('title', 'Unknown Media'),
                'thumbnail': info.get('thumbnail'),
                'uploader': info.get('uploader', 'Unknown Creator'),
                'duration': info.get('duration')
            }
    except Exception:
        return None


def download_media(url, format_choice="Best Quality", platform="Generic", cookie_path=None, browser=None):
    output_dir = "downloads"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    unique_id = uuid.uuid4().hex[:6]

    if platform == "Spotify":
        search_query = convert_spotify_to_ytsearch(url)
        if not search_query:
            return None, None
        url = search_query
        format_choice = "Audio Only (MP3)"

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

    if browser and browser != "None":
        ydl_opts['cookiesfrombrowser'] = (browser.lower(),)
    elif cookie_path and os.path.exists(cookie_path):
        ydl_opts['cookiefile'] = cookie_path

    if format_choice == "Audio Only (MP3)" or platform == "Spotify":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            if 'entries' in info_dict:
                info_dict = info_dict['entries'][0]

            if format_choice == "Audio Only (MP3)":
                final_file_path = os.path.splitext(ydl.prepare_filename(info_dict))[0] + ".mp3"
            else:
                ext = ydl.prepare_filename(info_dict)
                base = os.path.splitext(ext)[0]
                if not os.path.exists(ext):
                    for possible_ext in ['.mp4', '.mkv', '.webm']:
                        if os.path.exists(base + possible_ext):
                            final_file_path = base + possible_ext
                            break
                    else:
                        final_file_path = ext
                else:
                    final_file_path = ext

            return final_file_path, info_dict.get('title', 'Media File')
    except Exception as e:
        st.error(f"Extraction Error: {e}")
        return None, None