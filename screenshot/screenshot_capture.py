import os
from sched import scheduler
import sys
import datetime
import yaml
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger



BIN_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../bin")

YT_DLP_BIN_PATH = os.path.join(BIN_PATH, "yt-dlp")



class YoutubeLiveScreenshot:
    def __init__(self, yml_file):
        config = yaml.safe_load(yml_file)
        self.config = config

        self.scheduler = BlockingScheduler()
        # self.scheduler = BackgroundScheduler() # これつかうならmain関数の最後にself.scheduler.wait()を追加する必要がある

        self.scheduler_add_job()

        self.update_bin()
        # 半日ごとに実行するジョブを追加
        self.scheduler.add_job(self.update_bin, IntervalTrigger(hours=12))

    def update_bin(self):
        #yt-dlpをアップデート
        subprocess.run([YT_DLP_BIN_PATH, "-U"])

    @staticmethod
    def yaml_parse(func):
        def wrapper(self):
            config = self.config

            for stream in config['stream_list']:
                func(self, stream)

        return wrapper

    def take_screenshot(self, name, url, output_path):
        
        # yt-dlpを使用してストリームのURLを取得
        stream_url = subprocess.run([YT_DLP_BIN_PATH, '-g', url], capture_output=True, text=True).stdout

        # 4Kダウンロードできるが12時間前の画像になる上、先頭からダウンロードするため負荷が大きい
        # 1080pを超えるダウンロードはHLSでない関係(yt-dlpもDASHは部分的なサポート?)とかで、安定を求めるならやめたほうがいいかも
        # stream_url = subprocess.run([YT_DLP_BIN_PATH, '-g', url, "-f 313", "--live-from-start"], capture_output=True, text=True).stdout

        # 現在の日時を取得
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(stream_url)
        os.makedirs(output_path, exist_ok=True)

        # ffmpegを使用してスクリーンショットを取得
        subprocess.run(["ffmpeg", "-i", stream_url, "-vframes", "1", os.path.join(output_path, f"screenshot_{timestamp}.jpg")])


        print(f"{name}: Screenshot taken at {timestamp} and saved to {output_path}")

    @yaml_parse
    def scheduler_add_job(self, stream):
        print(stream)
        self.scheduler.add_job(self.take_screenshot, args=[stream['name'], stream['stream_url'], stream['save_path']], trigger=CronTrigger.from_crontab(stream['crontab']))

if __name__ == "__main__":

    with open("config.yml") as file:
        yls = YoutubeLiveScreenshot(file)
        yls.scheduler.start()