from PyQt5 import QtWidgets, QtCore, QtGui

import webbrowser
import sys
import os


MAIN_ICON_PATH = r'Files\icon.ico'
BACKSPACE_ICON_PATH = r'Files\backspace.png'


class AboutDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        if sys.platform == 'win32':
            import winsound
            winsound.MessageBeep()

        self.setupUi()

    def setupUi(self):
        self.setWindowIcon(QtGui.QIcon(MAIN_ICON_PATH))
        self.setFixedSize(300, 100)
        self.setWindowTitle("About us")

        description = QtWidgets.QLabel(self)
        description.setGeometry(75, 10, 150, 30)
        description.setText("This program made by Sina.F")

        horizontal_frame = QtWidgets.QWidget(self)
        horizontal_frame.setGeometry(15, 50, 270, 40)
        horizontal_layout = QtWidgets.QHBoxLayout(horizontal_frame)
        horizontal_layout.setContentsMargins(40, 0, 40, 0)
        horizontal_layout.setSpacing(15)

        btn_github = QtWidgets.QPushButton(horizontal_frame)
        btn_github.setText("GitHub")
        btn_github.clicked.connect(lambda: webbrowser.open('https://github.com/sina-programer'))

        btn_telegram = QtWidgets.QPushButton(horizontal_frame)
        btn_telegram.setText("Telegram")
        btn_telegram.clicked.connect(lambda: webbrowser.open('https://t.me/sina_programer'))

        horizontal_layout.addWidget(btn_github)
        horizontal_layout.addWidget(btn_telegram)


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator PyQt")
        self.setGeometry(500, 250, 310, 400)
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon(MAIN_ICON_PATH))


        self.monitor_font = QtGui.QFont("Consolas", 12)
        self.monitor_font.setBold(True)

        self.monitor = QtWidgets.QLineEdit(self)
        self.monitor.setGeometry(20, 40, 270, 45)
        self.monitor.setReadOnly(True)
        self.monitor.setAlignment(QtCore.Qt.AlignRight)
        self.monitor.setFont(self.monitor_font)

        brush = QtGui.QBrush(QtGui.QColor(155, 155, 155))
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        self.lbl_history = QtWidgets.QLabel(self)
        self.lbl_history.setGeometry(24, 42, 250, 15)
        self.lbl_history.setPalette(palette)


        WIDTH = 60
        HEIGHT = 30

        col1 = 0
        col2 = 70
        col3 = 140
        col4 = 210

        row1 = 0
        row2 = 40
        row3 = 80
        row4 = 120
        row5 = 160
        row6 = 200
        row7 = 240

        self.buttons_frame = QtWidgets.QFrame(self)
        self.buttons_frame.setGeometry(20, 110, 270, 270)
        self.buttons_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.buttons_frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.btn_parenthesesO = QtWidgets.QPushButton('(', self.buttons_frame)
        self.btn_parenthesesO.setGeometry(col1, row1, WIDTH, HEIGHT)
        self.btn_parenthesesO.setShortcut('(')

        self.btn_parenthesesC = QtWidgets.QPushButton(')', self.buttons_frame)
        self.btn_parenthesesC.setGeometry(col2, row1, WIDTH, HEIGHT)
        self.btn_parenthesesC.setShortcut(')')

        self.btn_clear = QtWidgets.QPushButton('C', self.buttons_frame)
        self.btn_clear.setGeometry(col3, row1, WIDTH, HEIGHT)
        self.btn_clear.setShortcut('c')

        backspace_icon = QtGui.QIcon()
        backspace_icon.addPixmap(QtGui.QPixmap(BACKSPACE_ICON_PATH), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_backspace = QtWidgets.QPushButton(self.buttons_frame)
        self.btn_backspace.setGeometry(QtCore.QRect(col4, row1, WIDTH, HEIGHT))
        if os.path.exists(BACKSPACE_ICON_PATH):
            self.btn_backspace.setIcon(backspace_icon)
        else:
            self.btn_backspace.setText('←')
        self.btn_backspace.setShortcut('backspace')

        self.btn_round = QtWidgets.QPushButton('R', self.buttons_frame)
        self.btn_round.setGeometry(col1, row2, WIDTH, HEIGHT)
        self.btn_round.setShortcut('r')

        self.btn_pow = QtWidgets.QPushButton('xʸ', self.buttons_frame)
        self.btn_pow.setGeometry(col2, row2, WIDTH, HEIGHT)
        self.btn_pow.setShortcut('^')

        self.btn_square = QtWidgets.QPushButton('x²', self.buttons_frame)
        self.btn_square.setGeometry(col3, row2, WIDTH, HEIGHT)

        self.btn_root = QtWidgets.QPushButton('²√', self.buttons_frame)
        self.btn_root.setGeometry(col4, row2, WIDTH, HEIGHT)

        self.btn_font = QtGui.QFont("Consolas", 11)
        self.btn_pi = QtWidgets.QPushButton('π', self.buttons_frame)
        self.btn_pi.setGeometry(col1, row3, WIDTH, HEIGHT)
        self.btn_pi.setShortcut('p')
        self.btn_pi.setFont(self.btn_font)

        self.btn_abs = QtWidgets.QPushButton('|x|', self.buttons_frame)
        self.btn_abs.setGeometry(col2, row3, WIDTH, HEIGHT)
        self.btn_abs.setShortcut('a')

        self.btn_reverse = QtWidgets.QPushButton('1/x', self.buttons_frame)
        self.btn_reverse.setGeometry(col3, row3, WIDTH, HEIGHT)

        self.btn_mul = QtWidgets.QPushButton('×', self.buttons_frame)
        self.btn_mul.setGeometry(col4, row3, WIDTH, HEIGHT)
        self.btn_mul.setShortcut('*')

        self.btn_7 = QtWidgets.QPushButton('7', self.buttons_frame)
        self.btn_7.setGeometry(col1, row4, WIDTH, HEIGHT)
        self.btn_7.setShortcut('7')

        self.btn_8 = QtWidgets.QPushButton('8', self.buttons_frame)
        self.btn_8.setGeometry(col2, row4, WIDTH, HEIGHT)
        self.btn_8.setShortcut('8')

        self.btn_9 = QtWidgets.QPushButton('9', self.buttons_frame)
        self.btn_9.setGeometry(col3, row4, WIDTH, HEIGHT)
        self.btn_9.setShortcut('9')

        self.btn_division = QtWidgets.QPushButton('÷', self.buttons_frame)
        self.btn_division.setGeometry(col4, row4, WIDTH, HEIGHT)
        self.btn_division.setShortcut('/')

        self.btn_4 = QtWidgets.QPushButton('4', self.buttons_frame)
        self.btn_4.setGeometry(col1, row5, WIDTH, HEIGHT)
        self.btn_4.setShortcut('4')

        self.btn_5 = QtWidgets.QPushButton('5', self.buttons_frame)
        self.btn_5.setGeometry(col2, row5, WIDTH, HEIGHT)
        self.btn_5.setShortcut('5')

        self.btn_6 = QtWidgets.QPushButton('6', self.buttons_frame)
        self.btn_6.setGeometry(col3, row5, WIDTH, HEIGHT)
        self.btn_6.setShortcut('6')

        self.btn_plus = QtWidgets.QPushButton('+', self.buttons_frame)
        self.btn_plus.setGeometry(col4, row5, WIDTH, HEIGHT)
        self.btn_plus.setShortcut('+')

        self.btn_1 = QtWidgets.QPushButton('1', self.buttons_frame)
        self.btn_1.setGeometry(col1, row6, WIDTH, HEIGHT)
        self.btn_1.setShortcut('1')

        self.btn_2 = QtWidgets.QPushButton('2', self.buttons_frame)
        self.btn_2.setGeometry(col2, row6, WIDTH, HEIGHT)
        self.btn_2.setShortcut('2')

        self.btn_3 = QtWidgets.QPushButton('3', self.buttons_frame)
        self.btn_3.setGeometry(col3, row6, WIDTH, HEIGHT)
        self.btn_3.setShortcut('3')

        self.btn_minus = QtWidgets.QPushButton('‒', self.buttons_frame)
        self.btn_minus.setGeometry(col4, row6, WIDTH, HEIGHT)
        self.btn_minus.setShortcut('-')

        self.btn_negative = QtWidgets.QPushButton('+/‒', self.buttons_frame)
        self.btn_negative.setGeometry(col1, row7, WIDTH, HEIGHT)

        self.btn_0 = QtWidgets.QPushButton('0', self.buttons_frame)
        self.btn_0.setGeometry(col2, row7, WIDTH, HEIGHT)
        self.btn_0.setShortcut('0')

        self.btn_dot = QtWidgets.QPushButton('.', self.buttons_frame)
        self.btn_dot.setGeometry(col3, row7, WIDTH, HEIGHT)
        self.btn_dot.setShortcut('.')

        self.btn_equal = QtWidgets.QPushButton('=', self.buttons_frame)
        self.btn_equal.setGeometry(col4, row7, WIDTH, HEIGHT)
        self.btn_equal.setShortcut('return')


        self._create_menu()

    def _create_menu(self):
        self.menuBar_main = self.menuBar()
        self.menuBar_main.addAction('About us', lambda: AboutDialog().exec_())
