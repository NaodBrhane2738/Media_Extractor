import os
import streamlit as st
from download_config import download_media, process_raw_cookies, get_media_info

st.set_page_config(page_title="Media Extractor", layout="centered")


def detect_platform(url):
    url = url.lower()
    if "youtube.com" in url or "youtu.be" in url: return "YouTube"
    if "instagram.com" in url: return "Instagram"
    if "tiktok.com" in url: return "TikTok"
    if "pinterest.com" in url or "pin.it" in url: return "Pinterest"
    if "spotify.com" in url: return "Spotify"
    return "Generic Site" if url.strip() else None


@st.cache_data(show_spinner=False)
def fetch_cached_preview(url, platform, cookie_path, browser):
    return get_media_info(url, platform, cookie_path, browser)


if 'files_to_cleanup' not in st.session_state:
    st.session_state.files_to_cleanup = []

for file_path in st.session_state.files_to_cleanup:
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass
st.session_state.files_to_cleanup = []

with st.sidebar:
    st.header("Configuration")
    format_choice = st.selectbox("Target Format",
                                 ["Best Quality (Video + Audio)", "Standard Quality (720p)", "Audio Only (MP3)"])

    st.divider()
    st.header("Authentication")
    st.caption("Required for platform-restricted content.")

    auth_method = st.radio("Method", ["None", "Import from Browser", "Upload File", "Paste Raw Data"])

    browser_selection = None
    manual_cookie_path = None

    if auth_method == "Import from Browser":
        browser_selection = st.selectbox("Select Browser", ["Chrome", "Firefox", "Brave", "Edge", "Opera"])

    elif auth_method == "Upload File":
        uploaded_file = st.file_uploader("Upload Cookie (.txt or .json)", type=['txt', 'json'])
        if uploaded_file and 'current_url' in st.session_state:
            content = uploaded_file.getvalue().decode("utf-8")
            file_ext = uploaded_file.name.split('.')[-1].lower()
            format_type = "JSON" if file_ext == 'json' else "Netscape"
            manual_cookie_path = process_raw_cookies(content, format_type, st.session_state.current_url)

    elif auth_method == "Paste Raw Data":
        cookie_format = st.selectbox("Data Format", ["JSON", "Netscape", "Header String"])
        raw_cookies = st.text_area("Paste Data")
        if raw_cookies and 'current_url' in st.session_state:
            manual_cookie_path = process_raw_cookies(raw_cookies, cookie_format, st.session_state.current_url)

st.title("Media Extractor")

media_url = st.text_input("Enter Media URL", placeholder="https://...")
st.session_state.current_url = media_url

if media_url:
    platform = detect_platform(media_url)

    with st.spinner("Retrieving metadata..."):
        info = fetch_cached_preview(media_url, platform, manual_cookie_path, browser_selection)

    if info:
        st.write("---")
        col1, col2 = st.columns([1, 2])

        with col1:
            if info.get('thumbnail'):
                st.image(info['thumbnail'], use_container_width=True)
            else:
                st.info("No thumbnail available.")

        with col2:
            st.subheader(info.get('title'))
            st.caption(f"Platform: {platform}")
            st.caption(f"Creator: {info.get('uploader')}")
            if info.get('duration'):
                mins, secs = divmod(int(info['duration']), 60)
                st.caption(f"Duration: {mins}:{secs:02d}")

            if platform == "Spotify" and "Video" in format_choice:
                st.warning("Spotify detected. Forcing Audio-Only extraction.")
    else:
        st.warning("Metadata unavailable. Check URL or authentication settings.")

    st.write("---")

    start_btn = st.button("Extract Media", type="primary", use_container_width=True)

    if start_btn:
        st.session_state['progress_bar'] = st.progress(0)
        st.session_state['status_text'] = st.empty()

        final_path, title = download_media(
            media_url,
            format_choice,
            platform,
            cookie_path=manual_cookie_path,
            browser=browser_selection
        )

        if final_path and os.path.exists(final_path):
            st.session_state['status_text'].empty()
            st.success("Extraction successful.")

            with open(final_path, "rb") as file_handler:
                st.download_button(
                    label=f"Download File",
                    data=file_handler,
                    file_name=os.path.basename(final_path),
                    mime="audio/mpeg" if final_path.endswith('.mp3') else "video/mp4",
                    use_container_width=True
                )

            st.session_state.files_to_cleanup.append(final_path)
            if manual_cookie_path and os.path.exists(manual_cookie_path):
                st.session_state.files_to_cleanup.append(manual_cookie_path)