Here is the updated, production-ready `README.md` reflecting the tool's evolution into a powerful, independent universal downloader.

I have updated the installation requirements to include the new scraping libraries, expanded the feature list to cover the cookie engine and live previews, and framed the description around building an independent, localized media toolset.

---

# Media Extractor

Media Extractor is an advanced, independent universal media downloader written in Python. Built to replace external software dependencies, it performs media stream extraction across multiple major platforms (YouTube, Instagram, TikTok, Pinterest, Spotify). The tool features a robust interactive web-based UI via Streamlit, providing live metadata previews, memory-safe file handling, and an advanced session authentication engine to securely access restricted content.

## Installation

1. Ensure you have Python 3 installed on your system.
2. Clone this repository (or download the script files):
```bash
git clone https://github.com/YOUR_USERNAME/MediaExtractor.git
cd MediaExtractor

```


3. Install the required Python dependencies:
```bash
pip install streamlit yt-dlp requests beautifulsoup4

```


4. (Optional but Recommended) Install FFmpeg for high-resolution stream merging:
```bash
winget install ffmpeg

```


*Note: The tool will work without FFmpeg but will be restricted to single-stream formats or audio-only extraction.*

## Usage

### Launching the Application

Run Media Extractor via your command line to launch the local web server:

```bash
streamlit run app.py

```

#### Interactive Options:

* **Target URL**: The media link (YouTube, Instagram, TikTok, Pinterest, Spotify).
* **Format**: Best Quality (Video + Audio), 720p, or Audio Only (MP3).
* **Authentication Method**: Import from Browser, Upload Cookie File (.json/.txt), or Paste Raw Data (Header Strings/Netscape).

### Execution Examples

Media Extractor is designed as a localized web-integrated script that automatically processes user inputs interactively. Launch the UI using `streamlit run app.py` and configure your extractions:

**Standard High-Fidelity Download** (YouTube):
Navigate to the web interface, select "Best Quality" and input:

```text
https://www.youtube.com/watch?v=L0v4jFMy5qA&pp=ygUlaSBrbm93IGkgY2FuIHRyZWF0IHlvdSBiZXR0ZXIgYmlsYWRlbg%3D%3D

```

**Follower-Only / Login-Walled Content** (Instagram/TikTok):
Select your desired format, expand the "Authentication" sidebar, select "Import from Browser" (e.g., Chrome), and input:

```text
https://www.instagram.com/p/EXAMPLE_POST/

```

**DRM Bypass / High-Quality Audio** (Spotify):
Select "Audio Only (MP3)" (the tool will auto-force this if a video format is chosen) and input:

```text
https://open.spotify.com/track/EXAMPLE_TRACK

```

### Core Features

* **Universal Platform Support**: Natively handles routing and extraction for YouTube, Instagram, TikTok, Pinterest, and Spotify.
* **Advanced Authentication Engine**: Securely bypasses login walls using dynamic cookie parsing (Supports raw JSON, Netscape, Header Strings, and direct DPAPI Browser extraction).
* **Live Metadata Previews**: Instantly fetches and displays video thumbnails, creators, and durations before initiating downloads.
* **Spotify DRM Routing**: Custom built-in web scraper that translates Spotify metadata into high-fidelity YouTube Music search queries to bypass encryption.
* **Memory-Safe Architecture**: Utilizes intelligent server-side file tracking and stream-based downloads to prevent RAM exhaustion.
* **Interactive Output**: Enhanced browser UI with Streamlit, keeping configurations in a clean sidebar and actions front-and-center.

### Security & Usage Notes

* **Responsibility**: Use this localized tool responsibly and only on media you own or have explicit permission to download.
* **Rate Limiting**: Social platforms (especially Instagram and TikTok) aggressively monitor traffic. Excessive bulk downloading may result in temporary IP or account bans.
* **Authentication Security**: The cookie extraction features handle your active session tokens. Ensure this tool is only run on trusted, secure local networks.
* **Compliance**: Be aware of the legal implications of downloading copyrighted media in your jurisdiction.

```

```
