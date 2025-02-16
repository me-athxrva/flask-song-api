from flask import jsonify
import os
from pathlib import Path

music_folder = "C:/Users/athar/Desktop/webdev/flask_music_api/backend/songs"
music_folder = Path(r"C:/Users/athar/Desktop/webdev/flask_music_api/backend/songs")

# Fetch full song list in directory
def getsongslist():
    songs = []
    for song in music_folder.iterdir():
        if song.suffix in ['.mp3', '.wav', '.flac']:
            song_name = song.stem
            songs.append({"name": song_name})
    return jsonify(songs)
    
# Get specific song
def getsong(song_name):
    for file in os.listdir(music_folder):
        if file.lower().endswith(('.mp3', '.wav', '.flac')):
            if os.path.splitext(file)[0].lower() == song_name.lower():  # Ignore case
                return os.path.join(music_folder, file)
    
    return None


    