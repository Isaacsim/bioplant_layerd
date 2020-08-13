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
import seaborn as sns
import matplotlib.pyplot as plt
import sys, os, settings
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from data import getRawData
from sklearn.linear_model import LinearRegression
from settings import PREDICTED_RANGE, LEARNING_RANGE, ROLLING_RANGE, ROLLING_RATIO


def PredictWindow(canvas, input_name, raw_data):

    data_tailed = raw_data.tail(LEARNING_RANGE)
    a1 = canvas.add_subplot(1, 1, 1)
    a1.cla()

    tail_data = data_tailed.iloc[-1]
    append_data = pd.DataFrame()
    append_data = append_data.append(tail_data)
    for n in range(0, ROLLING_RANGE):
        tail = append_data.iloc[-1]
        tail["Time"] += ROLLING_RATIO
        append_data = append_data.append(tail)

    data_tailed_rolling = data_tailed.append(append_data, sort=False)
    print(data_tailed_rolling)

    # a1.plot(cancer["Time"].tail(30), cancer[input_name].tail(30))
    linreg = LinearRegression()
    x = np.c_[
        data_tailed_rolling["Time"].values.reshape(-1, 1),
        (data_tailed_rolling["Time"].values.reshape(-1, 1)) ** 2,
        (data_tailed_rolling["Time"].values.reshape(-1, 1)) ** 3,
    ]
    y = data_tailed_rolling[input_name].values.reshape(-1, 1)
    model = linreg.fit(x, y)
    intercept = model.intercept_
    coef = model.coef_
    print(intercept, coef)

    xs = np.arange(
        data_tailed_rolling.iloc[0, 0],
        data_tailed_rolling.iloc[-1, 0] + PREDICTED_RANGE,
        1,
    )
    ys = (
        xs * model.coef_[0, 0]
        + (xs ** 2) * model.coef_[0, 1]
        + (xs ** 3) * model.coef_[0, 2]
        + model.intercept_[0]
    )

    ys_ci = (
        0.2
        * ys ** 2
        / np.mean(ys)
        * np.sqrt(1 / n + (ys - np.mean(ys)) ** 2 / np.sum((ys - np.mean(ys)) ** 2))
    )
    a1.scatter(x="Time", y=input_name, color="b", data=data_tailed)
    a1.plot(xs, ys, lw=1, color="r")
    a1.fill_between(xs, ys - ys_ci, ys + ys_ci, color="r", alpha=0.1)
    a1.axvline(x=tail_data["Time"], color="black")

    a1.set_title(f"Raw data versus predicted value, {input_name}")
    a1.legend(["predicted graph", "latest append date", "raw data"], loc="upper left")
    a1.set_xlabel("Time(days)")
    a1.set_ylabel(input_name)
    a1.grid(True)

    return a1

