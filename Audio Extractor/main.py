from PyQt5 import QtGui, QtWidgets
from moviepy import editor
import webbrowser
import sys
import os


class AboutDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setup_Ui()

    def setup_Ui(self):
        self.setWindowTitle("About us")
        self.setWindowIcon(QtGui.QIcon(ICON_PATH))
        self.setFixedSize(300, 100)

        description = QtWidgets.QLabel(self)
        description.setGeometry(75, 10, 150, 30)
        description.setText("This program made by Sina.F")


        horizontal_frame = QtWidgets.QWidget(self)
        horizontal_frame.setGeometry(50, 50, 200, 40)

        horizontal_layout = QtWidgets.QHBoxLayout(horizontal_frame)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.setSpacing(15)

        btn_github = QtWidgets.QPushButton(horizontal_frame)
        btn_github.clicked.connect(lambda: webbrowser.open('https://github.com/sina-programer'))
        btn_github.setText("GitHub")
        horizontal_layout.addWidget(btn_github)

        btn_telegram = QtWidgets.QPushButton(horizontal_frame)
        btn_telegram.clicked.connect(lambda: webbrowser.open('https://t.me/sina_programer'))
        btn_telegram.setText("Telegram")
        horizontal_layout.addWidget(btn_telegram)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.aboutDialog = AboutDialog()
        self.video = None
        self.setup_Ui()
        self.show()

    def setup_Ui(self):
        self.setWindowTitle("Audio Extractor")
        self.setWindowIcon(QtGui.QIcon(ICON_PATH))
        self.setFixedSize(550, 90)

        browse_btn = QtWidgets.QPushButton(self)
        browse_btn.setGeometry(20, 40, 80, 30)
        browse_btn.setText("Browse")
        browse_btn.clicked.connect(self.browse)

        self.video_path = QtWidgets.QLineEdit(self)
        self.video_path.setGeometry(110, 45, 300, 20)
        self.video_path.setReadOnly(True)
        self.video_path.setPlaceholderText("Video path")

        extract_btn = QtWidgets.QPushButton(self)
        extract_btn.setGeometry(430, 40, 100, 30)
        extract_btn.setText("Extract Audio")
        extract_btn.clicked.connect(self.extract_audio)

        self.init_menu()

    def extract_audio(self):
        if self.video:
            save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Audio File', '', "Audio Files (*.mp3)")
            if save_path:
                self.video.audio.write_audiofile(save_path)
                self.video.close()

                QtWidgets.QMessageBox.information(self, 'Audio Extracted', '\nAudio of your file successfully exported!\t\n')

        else:
            QtWidgets.QMessageBox.critical(self, 'ERROR', '\nPlease first load a video!\t\n')

    def browse(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Video File', '', "Video Files (*.mp4)")
        if path:
            path = os.path.normpath(path)
            self.video = editor.VideoFileClip(path)
            self.video_path.setText(path)

    def init_menu(self):
        aboutAction = QtWidgets.QAction('About us', self)
        aboutAction.triggered.connect(lambda: self.aboutDialog.exec_())

        menu = self.menuBar()
        menu.addAction(aboutAction)



ICON_PATH = 'icon.ico'


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()

    sys.exit(app.exec_())
