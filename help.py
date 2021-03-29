
from PyQt5.QtWidgets import QWidget, QTextBrowser, QHBoxLayout

class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.getHelpText()

    def initUI(self):
        self.textbox_help_1 = QTextBrowser()
        layout = QHBoxLayout()
        layout.addWidget(self.textbox_help_1)
        self.setLayout(layout)

    def getHelpText(self):
        f = open("help.txt", mode="r", encoding="utf-8")
        for line in f:
            self.textbox_help_1.append(line)

