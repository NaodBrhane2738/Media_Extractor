import streamlit as st
import os
from download_config import download_youtube_video

st.set_page_config(page_title="Advanced YT Downloader", page_icon="🚀", layout="centered")

# --- Smart Server Cleanup System ---
if 'files_to_cleanup' not in st.session_state:
    st.session_state.files_to_cleanup = []

# Delete previous files to save server space when the app reruns
for file_path in st.session_state.files_to_cleanup:
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass
st.session_state.files_to_cleanup = []  # Reset tracker after cleanup

# --- UI Setup ---
st.title("🚀 Advanced YouTube Downloader")
st.markdown("Download videos with enhanced features: custom formats, real-time progress, and safe memory handling.")

with st.sidebar:
    st.header("⚙️ Settings")
    video_url = st.text_input("Enter YouTube Video URL:")
    format_choice = st.selectbox(
        "Select Format:",
        ["Best Quality (Video + Audio)", "Standard Quality (720p)", "Audio Only (MP3)"]
    )
    start_btn = st.button("Start Processing", type="primary", use_container_width=True)

if start_btn:
    if not video_url.strip():
        st.warning("⚠️ Please enter a valid YouTube URL in the sidebar.")
    else:
        st.info(f"🔗 Processing: `{video_url}`")

        # Placeholders for the live progress hook
        st.session_state['progress_bar'] = st.progress(0)
        st.session_state['status_text'] = st.empty()

        # Call the improved backend function
        final_path, title = download_youtube_video(video_url, format_choice)

        if final_path and os.path.exists(final_path):
            st.session_state['status_text'].empty()
            st.success("✅ Processed successfully! Ready for download.")

            # Use file handler for memory efficiency (no f.read() crash)
            with open(final_path, "rb") as file_handler:
                file_name = os.path.basename(final_path)
                mime_type = "audio/mpeg" if "Audio Only" in format_choice else "video/mp4"

                st.download_button(
                    label=f"⬇️ Download: {title}",
                    data=file_handler,  # Passed directly for RAM efficiency
                    file_name=file_name,
                    mime=mime_type,
                    use_container_width=True
                )

            # Queue file for deletion on the NEXT interaction to prevent breaking the download button
            st.session_state.files_to_cleanup.append(final_path)