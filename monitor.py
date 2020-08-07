from PyQt5.QtWidgets import QWidget, QGroupBox, QRadioButton, QPushButton, QHBoxLayout, QVBoxLayout, QApplication
from PyQt5 import uic
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
import pandas as pd
import sys, os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

MONITOR_INPUT_LIST = ["VFA", "Alk", "VFA/Alk", "Biogas Production", "Biogas Yield", "VSRem"]
MONITOR_PLOT_LIST = ["예측", "추세"]
raw_data = pd.read_csv('raw_data.csv')




class MonitorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()        

    def initUI(self):
        self.monitor_inputs = []
        for i in range(0, len(MONITOR_INPUT_LIST)):
            self.monitor_inputs.append(QRadioButton(MONITOR_INPUT_LIST[i]))
        self.monitor_plots = []
        for i in range(0, len(MONITOR_PLOT_LIST)):
            self.monitor_plots.append(QRadioButton(MONITOR_PLOT_LIST[i]))
        self.monitor_inputs[0].setChecked(True)
        self.monitor_plots[1].setChecked(True)
        self.valueGroupBox = QGroupBox("출력 변수 선택")
        self.outputGroupBox = QGroupBox("출력 그래프 선택")
        self.pushButton_monitor = QPushButton("출력")        

        self.btnInputLayout = QHBoxLayout()
        for i in range(0, len(self.monitor_inputs)):
            self.btnInputLayout.addWidget(self.monitor_inputs[i])
        self.valueGroupBox.setLayout(self.btnInputLayout)

        self.btnOutputLayout = QHBoxLayout()
        for i in range(0, len(self.monitor_plots)):
            self.btnOutputLayout.addWidget(self.monitor_plots[i])
        self.outputGroupBox.setLayout(self.btnOutputLayout)        

        self.inputLayout = QHBoxLayout()
        self.inputLayout.addWidget(self.valueGroupBox)
        self.inputLayout.addWidget(self.outputGroupBox)
        self.inputLayout.addWidget(self.pushButton_monitor)

        self.outputLayout = QHBoxLayout()       
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.outputLayout.addWidget(self.canvas)
     
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.inputLayout)
        self.layout.addLayout(self.outputLayout)
     
        self.setLayout(self.layout)
      
        self.pushButton_monitor.clicked.connect(self.setMonitor)

        #모니터부분 피규어 출력 부분 설정
        
    def setMonitor(self):
        input_name = self.getMonitorInput()
        plot_name = self.getMonitorPlot()
        if plot_name == "예측" :
            self.setMonitorPredicted(input_name)
        elif plot_name == "추세" :
            self.setMonitorEstimated(input_name)
            
    def getMonitorInput(self):
        for i in range(0, len(self.monitor_inputs)):
            if self.monitor_inputs[i].isChecked() :
                print(self.monitor_inputs[i].text())
                return self.monitor_inputs[i].text()

    def getMonitorPlot(self):
        for i in range(0, len(self.monitor_plots)):
            if self.monitor_plots[i].isChecked() :
                print(self.monitor_plots[i].text())
                return self.monitor_plots[i].text()

    def setMonitorEstimated(self, input_name):
        global raw_data
        print(raw_data.columns)
        for i in range(0,len(MONITOR_INPUT_LIST)):
            if raw_data.columns[i+2] == MONITOR_INPUT_LIST[i]:
                print("Corretn")
        ax = self.fig.add_subplot(1, 1, 1)
        ax.cla()
        ax.set_title(f"Raw data versus estimated trend, {input_name}")
        x = raw_data["Time"]
        y = raw_data[input_name]
        f = raw_data[input_name].rolling(window=10, center=True).mean()
        ax.plot(x, y, '-b', x, f, '--r', linewidth = 0.8)
        ax.plot(x, f, '--r', linewidth = 1.5)
        ax.legend(["raw data", "estimated trend"], loc='upper left')
        ax.set_xlabel("Time(days)")
        ax.set_ylabel(input_name)
        
        ax.grid(True)
        self.canvas.draw()

    def setMonitorPredicted(self, input_name):
        global raw_data
        pass
            
