import os
import requests
from PyQt6.QtCore import QObject, pyqtSignal

class VideoDownloader(QObject):
    progress_updated = pyqtSignal(str, int, int)
    download_finished = pyqtSignal(str, bool)

    def __init__(self):
        super().__init__()

    def download(self, url, title, save_path):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = os.path.join(save_path, f"{clean_title}.mp4")
            
            file_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        self.progress_updated.emit(title, downloaded, file_size)
            
            self.download_finished.emit(title, True)
            return True
        except Exception as e:
            self.download_finished.emit(f"{title} - {str(e)}", False)
            return False 