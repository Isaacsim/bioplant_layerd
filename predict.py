import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from settings import PREDICTED_RANGE, LEARNING_RANGE, ROLLING_RANGE, ROLLING_RATIO


def PredictWindow(canvas, input_name, raw_data):

    data_tailed = raw_data.tail(LEARNING_RANGE)

    canvas.cla()

    tail_data = data_tailed.iloc[-1]
    append_data = pd.DataFrame()
    append_data = append_data.append(tail_data)

    #정확도 증가를 위한 padding과정
    for n in range(0, ROLLING_RANGE):
        tail = append_data.iloc[-1]
        tail["Time"] += ROLLING_RATIO
        append_data = append_data.append(tail)


    data_tailed_rolling = data_tailed.append(append_data, sort=False)

    # canvas.plot(cancer["Time"].tail(30), cancer[input_name].tail(30))
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
    #print(intercept, coef)

    xs = np.arange(
        data_tailed.iloc[0, 0],
        data_tailed.iloc[-1, 0] + PREDICTED_RANGE,
        1,
    )

    ys = (
        xs * model.coef_[0, 0]
        + (xs ** 2) * model.coef_[0, 1]
        + (xs ** 3) * model.coef_[0, 2]
        + model.intercept_[0]
    )

    ys_ci = (
        0.05
        * ys ** 2
        / np.mean(ys)
        * np.sqrt(1 / n + (ys - np.mean(ys)) ** 2 / np.sum((ys - np.mean(ys)) ** 2))
    )

    xs_s = xs[-PREDICTED_RANGE:]
    ys_s = ys[-PREDICTED_RANGE:]
    ys_ci_s = ys_ci[-PREDICTED_RANGE:]

    #print(np.mean(ys))
    for i in range(0, PREDICTED_RANGE):
        ys_ci[-PREDICTED_RANGE + i] *= (1 + i)
    #print(ys_ci[-5:-1])

    canvas.scatter(x="Time", y=input_name, color="b", data=data_tailed)
    canvas.plot(xs, ys, "--r", lw=1)
    canvas.fill_between(xs_s, ys_s - ys_ci_s, ys_s + ys_ci_s, color="r", alpha=0.1)
    canvas.axvline(x=tail_data["Time"], color="black", lw=3)
    canvas.plot(xs_s, ys_s, "c", lw=5)

    canvas.set_title(f"Raw data versus predicted value, {input_name}")
    canvas.legend(["estimated graph", "date of latest append data", "predicted graph", "raw data", "standard variation < 1"], loc="upper left")
    canvas.set_xlabel("Time(days)")
    canvas.set_ylabel(input_name)
    canvas.grid(True)

    return canvas

