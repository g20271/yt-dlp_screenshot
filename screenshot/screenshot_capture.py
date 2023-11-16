import os
import sys
import datetime
import yaml
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger



PATH = os.path.dirname(p=os.path.abspath(__file__))



class YoutubeLiveScreenshot:
    def __init__(self, yml_file):
        config = yaml.safe_load(yml_file)
        self.config = config

        self.scheduler = BlockingScheduler()

        self.scheduler_add_job()

    def yaml_parse(func):
        def wrapper(self):
            config = self.config

            for stream in config['stream_list']:
                func(self, stream)

        return wrapper

    def take_screenshot(self, url, output_path):
        #yt-dlpをアップデート
        subprocess.run([os.path.join(PATH, f"../bin/yt-dlp_linux"), "-U"])
        print
# '-f', 'bestvideo[height<=2160]+bestaudio/best[height<=2160]', 
        # yt-dlpを使用してストリームのURLを取得
        stream_url = subprocess.run([os.path.join(PATH, f"../bin/yt-dlp_linux"), '-g', url], capture_output=True, text=True).stdout

        # 現在の日時を取得
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(stream_url)
        os.makedirs(output_path, exist_ok=True)

        # ffmpegを使用してスクリーンショットを取得
        subprocess.run(["ffmpeg", "-i", stream_url, "-ss", "00:00:05", "-vframes", "1", os.path.join(output_path, f"screenshot_{timestamp}.jpg")])

    @yaml_parse
    def scheduler_add_job(self, stream):
        print(stream)
        self.scheduler.add_job(self.take_screenshot, args=[stream['stream_url'], stream['save_path']], trigger=CronTrigger.from_crontab(stream['crontab']))

if __name__ == "__main__":

    with open("data/config.yml") as file:
        yls = YoutubeLiveScreenshot(file)
        yls.take_screenshot("https://www.youtube.com/watch?v=jfKfPfyJRdk", "data")
        yls.scheduler.start()