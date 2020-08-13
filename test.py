import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget,
    QGroupBox,
    QRadioButton,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QMessageBox,
    QSpinBox,
    QLabel,
    QTableView,
    QTextBrowser,
)
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
import sys, os, settings
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from data import getRawData
from sklearn.linear_model import LinearRegression
from settings import PREDICTED_RANGE, LEARNING_RANGE, ROLLING_RANGE


def testPlot(canvas, input_name):
    a1 = canvas.add_subplot(1, 1, 1)

    cancer = pd.read_csv("raw_data.csv")
    cancer_tailed = cancer.tail(LEARNING_RANGE)
    tail_data = cancer_tailed.iloc[-1]
    append_data = pd.DataFrame()
    append_data = append_data.append(tail_data)
    for n in range(0, ROLLING_RANGE + 1):
        tail = append_data.iloc[-1]
        tail["Time"] += 1
        append_data = append_data.append(tail)
    print(append_data)

    # a1.plot(cancer["Time"].tail(30), cancer["OLR"].tail(30))
    a1.scatter(x="Time", y="OLR", data=cancer_tailed)

    linreg = LinearRegression()
    x = np.c_[
        cancer_tailed["Time"].values.reshape(-1, 1),
        (cancer_tailed["Time"].values.reshape(-1, 1)) ** 2,
        (cancer_tailed["Time"].values.reshape(-1, 1)) ** 3,
    ]
    y = cancer_tailed["OLR"].values.reshape(-1, 1)
    model = linreg.fit(x, y)
    intercept = model.intercept_
    coef = model.coef_
    print(intercept, coef)

    xs = np.arange(
        cancer_tailed.iloc[0, 0], cancer_tailed.iloc[-1, 0] + PREDICTED_RANGE, 0.1
    )
    ys = (
        xs * model.coef_[0, 0]
        + (xs ** 2) * model.coef_[0, 1]
        + (xs ** 3) * model.coef_[0, 2]
        + model.intercept_[0]
    )

    a1.plot(xs, ys, lw=3)

    return a1

