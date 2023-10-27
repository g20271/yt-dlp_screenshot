import os
import sys
import datetime
import subprocess

# ライブストリームのURLを指定
YOUTUBE_LIVE_URL = "https://www.youtube.com/watch?v=u6e_v5ntnyw"

# 現在の日時を取得
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

PATH = os.path.dirname()

print(PATH)

#yt-dlpをアップデート
subprocess.run(PATH + f"../bin/yt-dlp_linux -U")

# yt-dlpを使用してストリームのURLを取得
stream_url = subprocess.getoutput(PATH + f"../bin/yt-dlp_linux -g {YOUTUBE_LIVE_URL}")

# ffmpegを使用してスクリーンショットを取得
subprocess.run(["ffmpeg", "-i", stream_url, "-ss", "00:00:05", "-vframes", "1", f"screenshot_{timestamp}.jpg"])
