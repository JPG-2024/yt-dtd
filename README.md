# YouTube Description Track Downloader

A Python script to download audio tracks from YouTube Description playlists.

## Features

- Extract video links from YouTube description playlists.
- Download audio tracks in MP3 format

## Installation

1. Clone this repository

2. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
# .\venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install playwright browsers:

```bash
playwright install
```

## Usage

Basic usage:

```bash
python track_dl.py <youtube_url>
```

## Requirements

- Python 3.7+
- yt-dlp
- playwright
- beautifulsoup4
