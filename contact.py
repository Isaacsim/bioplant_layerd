import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ContactWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.getContactText()

    def initUI(self):
        self.textbox_contact_1 = QTextBrowser()
        layout = QHBoxLayout()
        layout.addWidget(self.textbox_contact_1)
        self.setLayout(layout)

    def getContactText(self):
        f = open("contact.txt", mode="r", encoding="utf-8")
        for line in f:
            self.textbox_contact_1.append(line)
