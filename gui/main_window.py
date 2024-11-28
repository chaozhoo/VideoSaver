import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QTextEdit, QFileDialog, QLabel, QProgressBar)
from .download_thread import DownloadThread
from utils.file_handler import load_style

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Saver 原链视频下载器")
        self.setMinimumSize(600, 400)
        self.save_path = os.path.join(os.getcwd(), "downloads")
        self.init_ui()
        self.load_style()
        self.download_threads = []

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # 路径选择区域
        path_layout = QHBoxLayout()
        self.path_label = QLabel(f"保存路径: {self.save_path}")
        path_layout.addWidget(self.path_label)
        path_btn = QPushButton("选择路径")
        path_btn.clicked.connect(self.choose_path)
        path_layout.addWidget(path_btn)
        layout.addLayout(path_layout)

        # 链接输入区域
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('请输入视频原始链接，支持批量下载，格式：\n"标题1","链接1";\n"标题2","链接2";')
        layout.addWidget(self.text_edit)

        # 下载按钮
        self.download_btn = QPushButton("开始下载")
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)

        # 进度显示
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

    def load_style(self):
        style = load_style('main.qss')
        if style:
            self.setStyleSheet(style)

    def choose_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if dir_path:
            self.save_path = dir_path
            self.path_label.setText(f"保存路径: {self.save_path}")

    def start_download(self):
        content = self.text_edit.toPlainText().strip()
        if not content:
            self.status_label.setText("请输入下载链接！")
            return

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        entries = [entry.strip() for entry in content.split(';') if entry.strip()]
        
        for entry in entries:
            try:
                parts = entry.split('","')
                if len(parts) != 2:
                    continue
                    
                title = parts[0].strip('"')
                url = parts[1].strip('"')
                
                thread = DownloadThread(url, title, self.save_path)
                thread.downloader.progress_updated.connect(self.update_progress)
                thread.downloader.download_finished.connect(self.download_finished)
                self.download_threads.append(thread)
                thread.start()
                
            except Exception as e:
                self.status_label.setText(f"错误: {str(e)}")

    def update_progress(self, title, downloaded, total):
        progress = int((downloaded / total) * 100)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(progress)
        self.status_label.setText(f"正在下载: {title}")

    def download_finished(self, title, success):
        if success:
            self.status_label.setText(f"下载完成: {title}")
        else:
            self.status_label.setText(f"下载失败: {title}") 