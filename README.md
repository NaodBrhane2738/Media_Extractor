# YoutubePY

YTPY is an advanced YouTube video downloader written in Python. It performs media stream extraction on target URLs, attempts to grab high-quality video and audio files, and provides memory-safe file handling. The tool supports a fully interactive web-based user interface (UI) mode via Streamlit.

## Installation

1. Ensure you have Python 3 installed on your system.
2. Clone this repository (or download the script files):
```
git clone https://github.com/NaodBrhane2738/YoutubePY.git
cd YoutubePY

```


3. (Optional) Install FFmpeg for enhanced high-resolution stream merging:

```
   winget install ffmpeg

```

Note: The tool will work without FFmpeg but will be restricted to single-stream formats or audio-only extraction.

## Usage

### Command-Line Mode

Run YTPY via your command line to launch the local application:

```bash
streamlit run app.py

```

#### Options:

* `Target URL`: YouTube video link (entered via UI)
* `Format`: Best Quality, 720p, or MP3 (selected via UI)

### CLI Features

YTPY is designed as a web-integrated script that automatically launches a local server and detects user inputs interactively.

#### Running Interactive Mode

To launch the interactive web-based interface, simply run:

```bash
streamlit run app.py

```

#### Command-Line Scanning Examples

**Best Quality Download** (High fidelity video and audio):
Navigate to the web interface, select "Best Quality (Video + Audio)" and input:

```text
https://www.youtube.com/watch?v=L0v4jFMy5qA&pp=ygUlaSBrbm93IGkgY2FuIHRyZWF0IHlvdSBiZXR0ZXIgYmlsYWRlbg%3D%3D

```

**Stealthy Extraction** (Audio only, faster processing):
Select "Audio Only (MP3)" from the dropdown and input:

```text
https://www.youtube.com/watch?v=L0v4jFMy5qA&pp=ygUlaSBrbm93IGkgY2FuIHRyZWF0IHlvdSBiZXR0ZXIgYmlsYWRlbg%3D%3D

```

#### Additional Examples:

*(Input these configurations directly into the YTPY web interface)*

```bash
# Download standard quality to save storage space
Target: https://www.youtube.com/watch?v=L0v4jFMy5qA&pp=ygUlaSBrbm93IGkgY2FuIHRyZWF0IHlvdSBiZXR0ZXIgYmlsYWRlbg%3D%3D
Format: Standard Quality (720p)

# Download high-quality MP3 for local listening
Target: https://www.youtube.com/watch?v=L0v4jFMy5qA&pp=ygUlaSBrbm93IGkgY2FuIHRyZWF0IHlvdSBiZXR0ZXIgYmlsYWRlbg%3D%3D
Format: Audio Only (MP3)

```

### Interactive Mode

Run YTPY to enter interactive mode:

```bash
streamlit run app.py

```

In interactive mode, you'll be prompted to enter:

* Target YouTube URL
* Desired media format
* Command to initiate processing

### Features

* **Multi-threaded downloading**: Fast concurrent media fetching via yt-dlp
* **Metadata grabbing**: Attempts to retrieve accurate titles and extensions from streams
* **Memory context**: Provides safe file handling and intelligent server-side cleanup
* **Progress tracking**: Real-time progress bar display during downloads
* **Output formats**: Save results as MP4 or MP3
* **Cross-platform**: Works on Windows, Linux, and macOS
* **Interactive output**: Enhanced browser UI with Streamlit widgets

### Security Notes

* Use this tool responsibly and only on media you own or have permission to download
* YouTube may log connection attempts or rate-limit excessive downloads
* Be aware of the legal implications of downloading copyrighted media in your jurisdiction

```

```
