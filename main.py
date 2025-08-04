from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import yt_dlp
import os
import uuid

app = FastAPI()

@app.get("/")
def root():
    return {"message": "YouTube Downloader is running"}

@app.get("/download")
def download_video(url: str = Query(...), res: str = Query("360p")):
    try:
        video_id = str(uuid.uuid4())
        output_path = f"{video_id}.mp4"

        ydl_opts = {
            'format': f'bestvideo[height<={res[:-1]}]+bestaudio/best[height<={res[:-1]}]',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return FileResponse(path=output_path, filename=output_path, media_type='video/mp4')

    except Exception as e:
        return {"error": str(e)}
