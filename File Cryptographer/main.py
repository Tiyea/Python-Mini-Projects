from PyQt5 import QtGui, QtWidgets
from itertools import cycle
import webbrowser
import random
import string
import sys
import os


class AboutDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowIcon(QtGui.QIcon(MAIN_ICON_PATH))
        self.setFixedSize(250, 100)
        self.setWindowTitle("About us")

        description = QtWidgets.QLabel(self)
        description.setGeometry(60, 10, 150, 30)  # Geometry(start_x, start_y, width, height)
        description.setText("This program made by Sina.f")


        horizontal_frame = QtWidgets.QWidget(self)
        horizontal_frame.setGeometry(45, 50, 175, 40)

        horizontal_layout = QtWidgets.QHBoxLayout(horizontal_frame)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.setSpacing(15)

        btn_github = QtWidgets.QPushButton(horizontal_frame)
        btn_github.setText("GitHub")
        btn_github.clicked.connect(lambda: webbrowser.open('https://github.com/sina-programer'))

        btn_telegram = QtWidgets.QPushButton(horizontal_frame)
        btn_telegram.setText("Telegram")
        btn_telegram.clicked.connect(lambda: webbrowser.open('https://t.me/sina_programer'))

        horizontal_layout.addWidget(btn_github)
        horizontal_layout.addWidget(btn_telegram)


class Cryptographer:
    characters = string.ascii_letters + string.digits + string.hexdigits + string.ascii_uppercase + string.punctuation

    @staticmethod
    def cryptography(text: bytes, key: bytes):
        return bytes(a ^ b for a, b in zip(text, cycle(key)))

    @staticmethod
    def generate_key(n=128):
        return ''.join(random.sample(Cryptographer.characters, n))


class Widget(QtWidgets.QMainWindow):
    def __init__(self):
        super(Widget, self).__init__()
        self.cryptographer = Cryptographer()
        self.aboutDialog = AboutDialog()
        self.key = None

        self.setupUi()

    def setupUi(self):
        window_icon = QtGui.QIcon()
        window_icon.addPixmap(QtGui.QPixmap(MAIN_ICON_PATH))

        self.setFixedSize(580, 190)
        self.setWindowIcon(window_icon)
        self.setWindowTitle("File Cryptographer")

        key_frame = QtWidgets.QFrame(self)
        key_frame.setGeometry(440, 40, 120, 120)

        load_key_btn = QtWidgets.QPushButton(key_frame)
        load_key_btn.setGeometry(25, 40, 80, 30)
        load_key_btn.setText("Load KEY")
        load_key_btn.clicked.connect(self.load_key)

        generate_key_btn = QtWidgets.QPushButton(key_frame)
        generate_key_btn.setGeometry(25, 80, 80, 30)
        generate_key_btn.setText("Generate KEY")
        generate_key_btn.clicked.connect(self.generate_key)

        self.selected_key_lbl = QtWidgets.QLabel(key_frame)
        self.selected_key_lbl.setGeometry(25, 10, 100, 20)
        self.selected_key_lbl.setText("KEY: ")


        lineEdit_font = QtGui.QFont()
        lineEdit_font.setPointSize(10)
        lineEdit_font.setWeight(50)
        lineEdit_font.setKerning(True)

        tabWidget = QtWidgets.QTabWidget(self)
        tabWidget.setGeometry(20, 35, 400, 130)
        tabWidget.setMovable(True)


        encoderTab_icon = QtGui.QIcon(ENCRYPT_ICON_PATH)
        encoderTab = QtWidgets.QWidget()

        open_file_btn_encoderTab = QtWidgets.QPushButton(encoderTab)
        open_file_btn_encoderTab.setGeometry(290, 20, 80, 30)
        open_file_btn_encoderTab.setText("Open file")
        open_file_btn_encoderTab.clicked.connect(self.open_encode_file)

        encode_btn_encoderTab = QtWidgets.QPushButton(encoderTab)
        encode_btn_encoderTab.setGeometry(290, 60, 80, 30)
        encode_btn_encoderTab.setText("Encrypt")
        encode_btn_encoderTab.clicked.connect(self.encrypt)

        self.file_path_line_encoder_tab = QtWidgets.QLineEdit(encoderTab)
        self.file_path_line_encoder_tab.setGeometry(10, 20, 260, 30)
        self.file_path_line_encoder_tab.setFont(lineEdit_font)
        self.file_path_line_encoder_tab.setReadOnly(True)
        self.file_path_line_encoder_tab.setPlaceholderText("Path")


        decoderTab_icon = QtGui.QIcon(DECRYPT_ICON_PATH)
        decoderTab = QtWidgets.QWidget()

        open_file_btn_decoderTab = QtWidgets.QPushButton(decoderTab)
        open_file_btn_decoderTab.setGeometry(290, 20, 80, 30)
        open_file_btn_decoderTab.setText("Open file")
        open_file_btn_decoderTab.clicked.connect(self.open_decode_file)

        decode_btn_decoderTab = QtWidgets.QPushButton(decoderTab)
        decode_btn_decoderTab.setGeometry(290, 60, 80, 30)
        decode_btn_decoderTab.setText("Decrypt")
        decode_btn_decoderTab.clicked.connect(self.decrypt)

        self.file_path_line_decoder_tab = QtWidgets.QLineEdit(decoderTab)
        self.file_path_line_decoder_tab.setGeometry(10, 20, 260, 30)
        self.file_path_line_decoder_tab.setFont(lineEdit_font)
        self.file_path_line_decoder_tab.setReadOnly(True)
        self.file_path_line_decoder_tab.setPlaceholderText("Path")


        tabWidget.addTab(encoderTab, encoderTab_icon, '')
        tabWidget.setTabText(tabWidget.indexOf(encoderTab), "Encrypt ")
        tabWidget.setTabToolTip(tabWidget.indexOf(encoderTab), "You can encrypt\nyour files here")

        tabWidget.addTab(decoderTab, decoderTab_icon, '')
        tabWidget.setTabText(tabWidget.indexOf(decoderTab), "Decrypt  ")
        tabWidget.setTabToolTip(tabWidget.indexOf(decoderTab), "You can decrypt\nyour files here")


        self.init_menu()

    def encrypt(self):
        if self.key:
            file_path = self.file_path_line_encoder_tab.text()
            if file_path:

                save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Encrypted File', '', "Encrypted Files (*.encrypt)")
                if save_path:

                    with open(file_path, 'rb') as file:
                        data = file.read()

                    cryptograph = self.cryptographer.cryptography(data, self.key)

                    with open(save_path, 'wb') as file:
                        file.write(cryptograph)

            else:
                QtWidgets.QMessageBox.critical(self, 'ERROR', '\nPlease open a file for encrypt!\t\n')

        else:
            QtWidgets.QMessageBox.critical(self, 'ERROR', '\nPlease first load a KEY!\t\n')

    def decrypt(self):
        if self.key:
            file_path = self.file_path_line_decoder_tab.text()
            if file_path:

                save_path, _ = QtWidgets.QFileDialog.getSaveFileName()
                if save_path:

                    with open(file_path, 'rb') as handler:
                        data = handler.read()

                    cryptograph = self.cryptographer.cryptography(data, self.key)

                    with open(save_path, 'wb') as handler:
                        handler.write(cryptograph)

            else:
                QtWidgets.QMessageBox.critical(self, 'ERROR', '\nPlease open a file for decrypt!\t\n')

        else:
            QtWidgets.QMessageBox.critical(self, 'ERROR', '\nPlease first load a KEY!\t\n')

    def generate_key(self):
        key_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Key File', '', "Key Files (*.key)")

        if key_path:
            key = self.cryptographer.generate_key()

            with open(key_path, 'wb') as keyFile:
                keyFile.write(key.encode())

    def load_key(self):
        key_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Key File', '', "Key Files (*.key)")

        if key_path:
            key_name = os.path.basename(key_path)
            self.selected_key_lbl.setText(f'KEY:  {key_name}')

            with open(key_name, 'rb') as keyFile:
                self.key = keyFile.read()

    def open_encode_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        if file_path:
            self.file_path_line_encoder_tab.setText(os.path.normpath(file_path))

    def open_decode_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '', "Encrypted Files (*.encrypt)")
        if file_path:
            self.file_path_line_decoder_tab.setText(os.path.normpath(file_path))

    def init_menu(self):
        helpAction = QtWidgets.QAction('Help', self)
        helpAction.triggered.connect(lambda: QtWidgets.QMessageBox.information(self, 'Help', HELP_MSG))

        aboutAction = QtWidgets.QAction('About us', self)
        aboutAction.triggered.connect(lambda: self.aboutDialog.exec_())

        menu = self.menuBar()
        menu.addAction(helpAction)
        menu.addAction(aboutAction)



MAIN_ICON_PATH = r'Files\icon.ico'
ENCRYPT_ICON_PATH = r'Files\encrypt.ico'
DECRYPT_ICON_PATH = r'Files\decrypt.ico'
HELP_MSG = '''
1_ Load a key (if you don't have any key, first generate a key)
2_ Open a file for encrypt or decrypt
3_ Press the encrypt/decrypt button and choose desired save path
4_ Your file is ready now!
'''


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
