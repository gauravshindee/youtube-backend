import os
import subprocess
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow frontend requests from localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Directory to save downloaded videos
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)  # Ensure the folder exists

# ✅ Find yt-dlp path dynamically
YTDLP_PATH = shutil.which("yt-dlp")  # Get absolute path of yt-dlp

if not YTDLP_PATH:
    raise RuntimeError("yt-dlp is not installed. Please install it using: pip install yt-dlp")

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}

@app.get("/download/{video_id}")
def download_video(video_id: str):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    save_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

    try:
        # ✅ Use yt-dlp with full path
        subprocess.run(
            [YTDLP_PATH, "-f", "best", "-o", save_path, video_url],
            check=True
        )
        return {"message": "Download complete", "file_path": save_path}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
