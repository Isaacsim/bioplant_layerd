from PyQt5.QtWidgets import (
    QWidget,
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
import matplotlib.pyplot as plt
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from data import getRawData
from pdtable import PdTable
from settings import LOG_EXCUTE, LOG_ERROR

class AnalysisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.analysis_push_1 = QPushButton("부분 분석")
        self.analysis_push_2 = QPushButton("전체 분석")
        self.analysis_spin_1 = QSpinBox()
        self.analysis_label_1 = QLabel("주간 데이터")
        self.analysis_table_1 = QTableView()
        self.analysis_text_1 = QTextBrowser()

        self.analysis_spin_1.setMaximum(999)
        self.analysis_spin_1.setValue(20)

        self.leftLayout = QHBoxLayout()
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.leftLayout.addWidget(self.canvas)

        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.analysis_spin_1)
        self.rightLayout.addWidget(self.analysis_label_1)
        self.rightLayout.addWidget(self.analysis_push_1)
        self.rightLayout.addWidget(self.analysis_push_2)
        self.rightLayout.addWidget(self.analysis_table_1)
        self.rightLayout.addWidget(self.analysis_text_1)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.leftLayout, 3)
        self.layout.addLayout(self.rightLayout, 1)
        self.setLayout(self.layout)

        self.a1 = self.fig.add_subplot(3, 1, 1)
        self.a2 = self.fig.add_subplot(3, 1, 2)
        self.a3 = self.fig.add_subplot(3, 1, 3)

        self.analysis_push_1.clicked.connect(self.setAnalysisGraph)
        self.analysis_push_2.clicked.connect(self.setAllAnalysisGraph)


    def setAnalysisGraph(self):
        raw_data = getRawData()
        if len(raw_data) == 0:
            self.warnRawData()
            return
        term = self.analysis_spin_1.value()
        if term * 7 > len(raw_data):
            self.warnExceedData()
            return
        else:
            self.setAnalysisLeftGraph(term)
            self.setAnalysisRightGraph(term)
        print(f"{LOG_EXCUTE[6]} 기간 = {self.analysis_spin_1.value()}")


    def setAllAnalysisGraph(self):
        raw_data = getRawData()
        if len(raw_data) == 0:
            self.warnRawData()
            return
        term = 0
        self.setAnalysisLeftGraph(term)
        self.setAnalysisRightGraph(term)
        print(LOG_EXCUTE[7])

    def setAnalysisLeftGraph(self, term):
        raw_data = getRawData()
        if term == 0:
            x = raw_data
        else:
            x = raw_data.iloc[len(raw_data) - term * 7 : len(raw_data), :]


        self.a1.cla()
        x1 = x["Time"]
        y1 = x["OLR"]
        self.a1.plot(x1, y1, "-b", linewidth=0.8)
        self.a1.set_xlabel("Time(days)")
        self.a1.set_ylabel("OLR")
        plt.tight_layout(pad=0.5)
        self.a1.grid(True)

        self.a2.cla()
        x2 = x["Time"]
        y2 = x["Biogas Production"]
        self.a2.plot(x2, y2, "-r", linewidth=0.8)
        self.a2.set_xlabel("Time(days)")
        self.a2.set_ylabel("Biogas Production")
        plt.tight_layout(pad=0.5)
        self.a2.grid(True)

        self.a3.cla()
        x3 = x["Time"]
        x_shift = x.shift(1)
        x_shift=x_shift.fillna(0)
        y3 = (x["OLR"] - x_shift["OLR"]) / x["OLR"] * 100
        y4 = (
            (x["Biogas Production"] - x_shift["Biogas Production"])
            / x["Biogas Production"]
            * 100
        )
        self.a3.fill_between(x3, 0, y3, color="b", alpha=0.4)
        self.a3.fill_between(x3, 0, y4, color="r", alpha=0.4)
        self.a3.set_xlabel("Time(days)")
        self.a3.set_ylabel("Variation of OLR and BP")
        self.a3.legend(["OLR", "Biogas Production"], loc="lower left")
        self.a3.grid(True)
        self.canvas.draw()

        error = abs(y3 - y4).mean()
        total_input_mean = raw_data["OLR"].mean()
        total_output_mean = raw_data["Biogas Production"].mean()
        input_ratio = x["OLR"].mean() / total_input_mean * 100
        output_ratio = x["Biogas Production"].mean() / total_output_mean * 100

        error = round(error, 2)
        total_input_mean = round(total_input_mean, 2)
        total_output_mean = round(total_output_mean, 2)
        input_ratio = round(input_ratio, 2)
        output_ratio = round(output_ratio, 2)

        info_text = f"입력 대비 출력 상관 예측 정확도 : {100-error}%" \
                    f"\n입력 대비 출력 오차율 (일별) : {error}%" \
                    f"\n전체 데이터 평균 OLR 부하량 : {total_input_mean} kg VS/m3" \
                    f"\n전체 데이터 평균 Biogas 출하량 : {total_output_mean} Nm3/kg Vsadd" \
                    f"\n평균 대비 최근 OLR 부하량 비율 : {input_ratio}%" \
                    f"\n평균 대비 최근 BP 출하량 비율 : {output_ratio}%"

        self.analysis_text_1.setText(info_text)

    def setAnalysisRightGraph(self, term):
        raw_data = getRawData()
        if term == 0:
            x = raw_data.iloc[:, [0, 1, 5]]
        else:
            x = raw_data.iloc[len(raw_data) - term * 7 : len(raw_data), [0, 1, 5]]
        model = PdTable(x)
        self.analysis_table_1.setModel(model)

    def warnRawData(self):
        print(LOG_ERROR[0])
        QMessageBox.warning(self, "Warning", "Raw data를 가져와야 합니다.")

    def warnExceedData(self):
        print(LOG_ERROR[5])
        QMessageBox.warning(self, "Warning", "Raw data가 설정한 기간보다 적습니다")
