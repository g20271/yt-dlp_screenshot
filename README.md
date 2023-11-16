# yt-dlp_screenshot 🎥📸
Youtubeのライブ配信を一定時間ごとにjpgで落とせるツール

# 特徴 ✨
- わかりやすい(当社比)YAMLでの設定管理
- 複数ストリームのダウンロードに対応
  - 個別に設定を変更可能
- crontab形式での時間指定の記述に対応

# つかいかた 🚀
1. 📓 YAMLを書く  
config.yamlに取得したいライブ配信のURLを記述します。crontabの書き方についての詳細は検索してください。
以下はサンプルです:
```yaml
stream_list:
    - name: 父母ヶ浜
      stream_url: https://www.youtube.com/watch?v=u6e_v5ntnyw
      save_path: ./data/mitoyo
      crontab: "0-59/5 * * * *" # every 5 minutes
    - name: Clock
      stream_url: https://www.youtube.com/watch?v=DHOHZJNJIjI
      save_path: ./data/clock
      crontab: "0-59/1 * * * *" # every 1 minutes
    # - name: Lofi Girl
    #   stream_url: https://www.youtube.com/watch?v=jfKfPfyJRdk
    #   save_path: ./data/LofiGirl
    #   crontab: "* */2 * * *" # every 2 hours

```
  
2. 📦 binにyt-dlpを入れる  
   ここからバイナリをダウンロードして`yt-dlp`という名前で`bin`に入れる  
   [yt-dlp Release Files](https://github.com/yt-dlp/yt-dlp#release-files)

3. 🎬 ffmpegも入れる  
   `sudo apt install ffmpeg`

4. 🚀 実行する  
   `python3 screenshot_capture.py`

5. 🎉 Have Fun


# ToDo 📅
- [x] 複数ストリームダウンロード ✔️
- [ ] 実行時引数でyamlを指定できるように 🧰
- [ ] 4K対応 🖥️
- [ ] systemdのservice化 🚀
- [ ] take_screenshot関数をきれいに 📸✨
