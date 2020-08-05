import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys, os 
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


monitor_input = 0
monitor_input_list = ["VFA", "Alk", "VFA/Alk", "Biogas Production", "Biogas Yield", "VSRem"]
monitor_plot = 1
monitor_plot_list = ["예측", "추세"]


class MonitorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):    

        groupBox = QGroupBox("출력 변수 선택")
        radioButton_monitor_bp = QRadioButton("Bio Production")
        radioButton_monitor_by = QRadioButton("Biogas Yueld")
        radioButton_monitor_vsr = QRadioButton("VSRem")
        radioButton_monitor_vfa = QRadioButton("VFA")
        radioButton_monitor_alk = QRadioButton("Alk")
        radioButton_monitor_va = QRadioButton("VFA/Alk")

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(radioButton_monitor_bp)
        inputLayout.addWidget(radioButton_monitor_by)
        inputLayout.addWidget(radioButton_monitor_vsr)
        inputLayout.addWidget(radioButton_monitor_vfa)
        inputLayout.addWidget(radioButton_monitor_alk)
        inputLayout.addWidget(radioButton_monitor_va)
        groupBox.setLayout(inputLayout)

        outputLayout = QHBoxLayout()       
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        outputLayout.addWidget(self.canvas)

        self.layout = QVBoxLayout()
        self.layout.addLayout(inputLayout)
        self.layout.addLayout(outputLayout)        

        self.setLayout(self.layout)

        

        #모니터부분 피규어 출력 부분 설정
        


    def setMonitorInput(self, state, button):
        button_text = button.text()        
        for i in range(0, len(monitor_input_list)) :
            if monitor_input_list[i] == button_text:
                global monitor_input
                monitor_input = i
                print(monitor_input)                
        self.textEdit.setText(f"{str(button.text())} is selected")
        print(monitor_input)

    def setMonitorPlot(self, state, button):
        button_text = button.text()        
        for i in range(0, len(monitor_plot_list)) :
            if monitor_plot_list[i] == button_text:
                global monitor_plot
                monitor_plot = i
                print(monitor_plot)                
        self.textEdit.setText(f"{str(button.text())} is selected")
        print(monitor_plot)

    def setMonitorEstimated(self):
        raw_data = pd.read_csv(resource_path('raw_data.csv'))
        ax = self.fig.add_subplot(1, 1, 1)
        ax.cla()
        ax.set_title(f"Raw data versus estimated trend, {monitor_input_list[monitor_input]}")
        x = raw_data["Time"]
        y = raw_data[monitor_input_list[monitor_input]]
        f = raw_data[monitor_input_list[monitor_input]].rolling(window=10, center=True).mean()
        ax.plot(x, y, '-b', x, f, '--r', linewidth = 0.8)
        ax.plot(x, f, '--r', linewidth = 1.5)
        ax.legend(["raw data", "estimated trend"], loc='upper left')
        ax.set_xlabel("Time(days)")
        ax.set_ylabel(monitor_input_list[monitor_input])


        #if monitor_plot == 1:        
           # rcnt_line = self.getRecentLine(raw_data)
           # ax.plot(raw_data["Time"], rcnt_line)
        #elif monitor_plot == 0:
          #  self.textEdit.setText(f"예측 미지원")
          #  pass            
        
        ax.grid(True)
        self.canvas.draw()

    def getRecentLine(self, raw_data):
        return 
            
         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MonitorWindow()
    mywindow.show()
    app.exec_()