from PyQt6.QtCore import QThread
from core.downloader import VideoDownloader

class DownloadThread(QThread):
    def __init__(self, url, title, save_path):
        super().__init__()
        self.url = url
        self.title = title
        self.save_path = save_path
        self.downloader = VideoDownloader()

    def run(self):
        self.downloader.download(self.url, self.title, self.save_path) 