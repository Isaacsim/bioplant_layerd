import sys, os
from PyQt5.QtWidgets import *
from monitor import MonitorWindow
from contact import ContactWindow
from analysis import AnalysisWindow
from help import HelpWindow
from predict import PredictWindow
from data import DataWindow
from settings import *
import pandas as pd
import numpy as np
from pdtable import PdTable
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sklearn.linear_model import LinearRegression
import sklearn.utils._cython_blas


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_widget = MainTapWidget()
        self.setCentralWidget(self.table_widget)
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 1280, 720)
        self.show()
        print(LOG_EXCUTE[0])


class MainTapWidget(QWidget):
    def __init__(self):
        super().__init__()
        tab_monitor = MonitorWindow()
        tab_analysis = AnalysisWindow()
        tab_data = DataWindow()
        tab_contact = ContactWindow()
        tab_help = HelpWindow()
        tabs = QTabWidget()

        tabs.addTab(tab_monitor, "Monitor")
        tabs.addTab(tab_analysis, "Analysis")
        tabs.addTab(tab_data, "Data")
        tabs.addTab(tab_contact, "Contact")
        tabs.addTab(tab_help, "Help")

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    ex
    ex.show()
    sys.exit(app.exec_())
