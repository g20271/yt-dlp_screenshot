#!/bin/bash

# ライブストリームのURLを指定
YOUTUBE_LIVE_URL="https://www.youtube.com/watch?v=u6e_v5ntnyw"

# 現在の日時を取得
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# ffmpegを使用してスクリーンショットを取得
ffmpeg -i `yt-dlp -g $YOUTUBE_LIVE_URL` -ss 00:00:05 -vframes 1 "screenshot_$TIMESTAMP.jpg"