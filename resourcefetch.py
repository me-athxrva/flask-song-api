from flask import request, Response, send_file
from flask_restful import Resource
from modules import getsongslist, getsong
from auth import is_authenticated
import os
from urllib.parse import unquote

# Getting Songs
class GetSongsList(Resource):
    def post(self):
        if is_authenticated()==True:
            return getsongslist()
        else:
            return {'message':'user not authenticated'}, 401
        

# Fetch song name if user is authenticated        
class GetSong(Resource):
    def post(self):
        song_data = request.get_json()
        song_name = song_data['name']
        if is_authenticated()==True:
            return getsong(song_name)
        else:
            return None
    
# stream songs api
class StreamSong(Resource):
    def get(self, song_name):
        auth = is_authenticated()
        if not auth:
            return {"error": "User not authenticated"}, 401

        song_path = getsong(song_name) 

        if not song_path or not os.path.exists(song_path):
            return {"error": "Song not found"}, 404

        file_size = os.path.getsize(song_path)
        range_header = request.headers.get("Range")

        if range_header:
            try:
                range_start = int(range_header.replace("bytes=", "").split("-")[0])
            except ValueError:
                return {"error": "Invalid range request"}, 400
        else:
            range_start = 0  

        def generate():
            with open(song_path, "rb") as f:
                f.seek(range_start)
                while chunk := f.read(64*1024):  # Read in 64KB chunks
                    yield chunk

        headers = {
            "Content-Range": f"bytes {range_start}-{file_size-1}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size - range_start),
            "Content-Type": "audio/mpeg",
        }

        return Response(generate(), status=206, headers=headers)
