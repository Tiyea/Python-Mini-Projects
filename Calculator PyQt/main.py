from PyQt5 import QtCore, QtGui, QtWidgets
from functools import wraps
from math import pi, sqrt
import sys

import layout


def operator(func):

    @wraps(func)
    def wrapper(self):
        result = Calculator.evaluate(self.clause)
        if result is not None:
            self.clause = str(func(self, result))

    return wrapper



class Calculator:
    error_txt = 'ERROR: '
    replace_characters = {
        '×': '*',
        '÷': '/',
        '^': '**',
        '√': 'sqrt',
        'π': 'pi',
    }
    translator = str.maketrans(replace_characters)

    def __init__(self):
        self._clause = ''

        self.qapp = QtWidgets.QApplication.instance()
        if not self.qapp:
            self.qapp = QtWidgets.QApplication(sys.argv)

        self.layout = layout.ApplicationWindow()
        self.bindings()

    def run(self):
        self.layout.show()
        self.layout.activateWindow()
        self.layout.raise_()

        self.qapp.exec()

    def bindings(self):
        self.layout.btn_0.clicked.connect(lambda: self.add_character('0'))
        self.layout.btn_1.clicked.connect(lambda: self.add_character('1'))
        self.layout.btn_2.clicked.connect(lambda: self.add_character('2'))
        self.layout.btn_3.clicked.connect(lambda: self.add_character('3'))
        self.layout.btn_4.clicked.connect(lambda: self.add_character('4'))
        self.layout.btn_5.clicked.connect(lambda: self.add_character('5'))
        self.layout.btn_6.clicked.connect(lambda: self.add_character('6'))
        self.layout.btn_7.clicked.connect(lambda: self.add_character('7'))
        self.layout.btn_8.clicked.connect(lambda: self.add_character('8'))
        self.layout.btn_9.clicked.connect(lambda: self.add_character('9'))
        self.layout.btn_parenthesesO.clicked.connect(lambda: self.add_character('('))
        self.layout.btn_parenthesesC.clicked.connect(lambda: self.add_character(')'))
        self.layout.btn_pow.clicked.connect(lambda: self.add_character('^('))
        self.layout.btn_square.clicked.connect(lambda: self.add_character('^(2)'))
        self.layout.btn_root.clicked.connect(lambda: self.add_character('√('))
        self.layout.btn_pi.clicked.connect(lambda: self.add_character('π'))
        self.layout.btn_mul.clicked.connect(lambda: self.add_character('×'))
        self.layout.btn_division.clicked.connect(lambda: self.add_character('÷'))
        self.layout.btn_plus.clicked.connect(lambda: self.add_character('+'))
        self.layout.btn_minus.clicked.connect(lambda: self.add_character('-'))
        self.layout.btn_dot.clicked.connect(lambda: self.add_character('.'))

        self.layout.btn_clear.clicked.connect(self.clear_monitor)
        self.layout.btn_backspace.clicked.connect(self.backspace)
        self.layout.btn_round.clicked.connect(self.round_number)
        self.layout.btn_abs.clicked.connect(self.fabs)
        self.layout.btn_reverse.clicked.connect(self.reverse)
        self.layout.btn_negative.clicked.connect(self.negative)
        self.layout.btn_equal.clicked.connect(self.calculate)

    @staticmethod
    def evaluate(clause):
        if clause:
            try:
                return eval(clause.translate(Calculator.translator))

            except Exception:
                return None

    @property
    def clause(self):
        return self._clause

    @clause.setter
    def clause(self, value):
        self._clause = value

        if self._clause and (Calculator.evaluate(self._clause) is None):
            self.layout.monitor.setText(Calculator.error_txt + self._clause)

        else:
            self.layout.monitor.setText(self._clause)

    def add_character(self, text):
        self.clause += text

    def backspace(self):
        if self.clause:
            self.clause = self.clause[:-1]

    def calculate(self):
        result = Calculator.evaluate(self.clause)
        if result is not None:
            self.layout.lbl_history.setText(self.clause)
            self.clause = str(result)

    @operator
    def fabs(self, x):
        return abs(x)

    @operator
    def negative(self, x):
        return -x

    @operator
    def reverse(self, x):
        return 1 / x

    @operator
    def round_number(self, x):
        return round(x)

    def clear_monitor(self):
        self.clause = ''
        self.layout.lbl_history.setText('')



if __name__ == "__main__":
    app = Calculator()
    app.run()
