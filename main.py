import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QApplication, QVBoxLayout
from monitor import MonitorWindow
from contact import ContactWindow
from analysis import AnalysisWindow
from data import DataWindow
from settings import APP_NAME


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_widget = MainTapWidget()
        self.setCentralWidget(self.table_widget)
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 1280, 720)
        self.show()


class MainTapWidget(QWidget):
    def __init__(self):
        super().__init__()
        tab_monitor = MonitorWindow()
        tab_analysis = AnalysisWindow()
        tab_data = DataWindow()
        tab_contact = ContactWindow()
        tabs = QTabWidget()

        tabs.addTab(tab_monitor, "Monitor")
        tabs.addTab(tab_analysis, "Analysis")
        tabs.addTab(tab_data, "Data")
        tabs.addTab(tab_contact, "Contact")

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
