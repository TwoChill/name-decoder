import os
import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QStackedWidget,
        QLineEdit, QPushButton, QLabel, QGraphicsOpacityEffect, QMessageBox,
    )
    from PySide6.QtMultimediaWidgets import QVideoWidget
    from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
    from PySide6.QtCore import QUrl, QPropertyAnimation, Qt
    from PySide6.QtGui import QPixmap
except ImportError:
    import subprocess
    print("PySide6 is required but not installed.")
    answer = input("Install now? (y/n): ").strip().lower()
    if answer == 'y':
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PySide6"])
        print("Installed. Please rerun the script.")
    sys.exit(0)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_NUMBERS = {11, 22, 33}


def calculate_number(name: str) -> int:
    total = sum(((ord(c.upper()) - 65) % 9) + 1 for c in name if c.isalpha())
    while total > 9 and total not in MASTER_NUMBERS:
        total = sum(int(d) for d in str(total))
    return total


def fade_in(widget, duration=3000):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)
    anim = QPropertyAnimation(effect, b"opacity", widget)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setDuration(duration)
    anim.start()
    return anim


class MainScreen(QWidget):
    def __init__(self, on_convert, on_about):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)

        self.logo = QLabel()
        pixmap = QPixmap(os.path.join(BASE_DIR, '3.png'))
        if pixmap.isNull():
            self.logo.setText("[logo not found]")
        else:
            self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter your name')
        self.name_input.setFixedHeight(48)

        self.convert_btn = QPushButton('Convert')
        self.convert_btn.setFixedHeight(48)
        self.convert_btn.setStyleSheet(
            "QPushButton { background-color: #FC3030; color: white; font-weight: bold; border: none; }"
            "QPushButton:hover { background-color: #e02020; }"
        )
        self.convert_btn.clicked.connect(lambda: on_convert(self.name_input.text()))

        self.about_btn = QPushButton('About Numerology')
        self.about_btn.setFixedHeight(36)
        self.about_btn.setStyleSheet(
            "QPushButton { background-color: transparent; color: #888888; border: 1px solid #555555; }"
            "QPushButton:hover { color: #bbbbbb; border-color: #888888; }"
        )
        self.about_btn.clicked.connect(on_about)

        layout.addWidget(self.logo)
        layout.addWidget(self.name_input)
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.about_btn)

        self._anims = [fade_in(self.logo), fade_in(self.name_input), fade_in(self.convert_btn), fade_in(self.about_btn)]


class VideoScreen(QWidget):
    def __init__(self, on_finished):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)

        self.audio = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video_widget)
        self.player.mediaStatusChanged.connect(
            lambda status: on_finished() if status == QMediaPlayer.MediaStatus.EndOfMedia else None
        )

    def play(self, path: str):
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()

    def stop(self):
        self.player.stop()


class NameDecoderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NameDecoder')
        self.resize(800, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.main_screen = MainScreen(self.on_convert, self.on_about)
        self.video_screen = VideoScreen(self.return_to_main)

        self.stack.addWidget(self.main_screen)
        self.stack.addWidget(self.video_screen)

    def on_convert(self, name: str):
        if not name.strip():
            return
        number = calculate_number(name)
        video_path = os.path.join(BASE_DIR, f"{number}.mp4")
        if not os.path.exists(video_path):
            QMessageBox.warning(self, "Missing video", f"No video file found for number {number}.")
            return
        self.stack.setCurrentWidget(self.video_screen)
        self.video_screen.play(video_path)

    def on_about(self):
        video_path = os.path.join(BASE_DIR, "0.mp4")
        if not os.path.exists(video_path):
            QMessageBox.warning(self, "Missing video", "Numerology explanation video not found.")
            return
        self.stack.setCurrentWidget(self.video_screen)
        self.video_screen.play(video_path)

    def return_to_main(self):
        self.video_screen.stop()
        self.stack.setCurrentWidget(self.main_screen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NameDecoderApp()
    window.show()
    sys.exit(app.exec())
