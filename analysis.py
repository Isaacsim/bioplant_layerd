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
from pdtable import PdTable


class AnalysisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.analysis_push_1 = QPushButton("부분분석")
        self.analysis_push_2 = QPushButton("전체분석")
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

    def setAllAnalysisGraph(self):
        raw_data = getRawData()
        if len(raw_data) == 0:
            self.warnRawData()
            return
        term = 0
        self.setAnalysisLeftGraph(term)
        self.setAnalysisRightGraph(term)

    def setAnalysisLeftGraph(self, term):
        raw_data = getRawData()
        if term == 0:
            x = raw_data
        else:
            x = raw_data.iloc[len(raw_data)- term * 7:len(raw_data), :]        

        a1 = self.fig.add_subplot(3, 1, 1)
        a1.cla()
        x1 = x["Time"]
        y1 = x["OLR"]
        a1.plot(x1, y1, '-b', linewidth=0.8)
        a1.set_xlabel("Time(days)")
        a1.set_ylabel("OLR")
        plt.tight_layout(pad=0.5)
        a1.grid(True)

        a2 = self.fig.add_subplot(3, 1, 2)
        a2.cla()
        x2 = x["Time"]
        y2 = x["Biogas Production"]
        a2.plot(x2, y2, '-r', linewidth=0.8)
        a2.set_xlabel("Time(days)")
        a2.set_ylabel("Biogas Production")
        plt.tight_layout(pad=0.5)
        a2.grid(True)
        
        a3 = self.fig.add_subplot(3, 1, 3)
        a3.cla()
        x3 = x["Time"]
        x_shift = x.shift(2)
        y3 = (x["OLR"] - x_shift["OLR"]) / x["OLR"] * 100
        y4 = (x["Biogas Production"] - x_shift["Biogas Production"]) / x["Biogas Production"] * 100
        a3.bar(x3, y3, width=1.5, color='b')
        a3.bar(x3, y4, color='r')
        a3.set_xlabel("Time(days)")
        a3.set_ylabel("OLR / BP Ratio")
        a3.legend(["OLR", "Biogas Production"], loc='lower left')
        a3.grid(True)
        
        self.canvas.draw()
        
        error = round(abs(y3 - y4).mean(),2)
        total_input_mean = round(raw_data["OLR"].mean(), 2)
        total_output_mean = round(raw_data["Biogas Production"].mean(),2)
        input_ratio = round(float(x["OLR"].mean()) / total_input_mean * 100, 2)
        output_ratio = round(float(x["Biogas Production"].mean()) / total_output_mean * 100, 2)

        info_text = f"입력대비 출력 상관도 : {100-error}%\n입력 대비 출력 오차율 (일별) : {error}%\n전체 데이터 평균 OLR 부하량 : {total_input_mean} kg VS/m3\n전체 데이터 평균 Biogas 출하량 : {total_output_mean} Nm3/kg Vsadd\n평균대비 최근 OLR 부하량 비율 : {input_ratio}%\n평균대비 최근 BP 출하량 비율 : {output_ratio}%"

        print(info_text)
        self.analysis_text_1.setText(info_text)

    def setAnalysisRightGraph(self, term):
        raw_data = getRawData()
        if term == 0:
            x = raw_data.iloc[:, [1, 5]]
        else:
            x = raw_data.iloc[len(raw_data) - term * 7:len(raw_data), [1, 5]]        
        model = PdTable(x)
        self.analysis_table_1.setModel(model)

    def warnRawData(self):
        QMessageBox.warning(self, "Warning", "Raw data를 가져와야 합니다.")

    def warnExceedData(self):
        QMessageBox.warning(self, "Warning", "Raw data가 설정한 기간보다 적습니다")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnalysisWindow()
    window.show()
    app.exec_()