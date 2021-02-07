from copy import deepcopy
from pathlib import Path
import numpy as np
import youtube_dl


DOWNLOAD_OPTIONS = {
    "format": "bestaudio/best",
    "extractaudio": True,
    "audioformat": "mp3",
    "noplaylist": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}

def from_youtube(video_id: str, cache_path: Path):
    music_output = Path(cache_path, f"{video_id}.mp3")
    if not music_output.exists():
        options = deepcopy(DOWNLOAD_OPTIONS)
        options["outtmpl"] = str(music_output)
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
    return music_output
