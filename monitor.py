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

        valueGroupBox = QGroupBox("출력 변수 선택")
        radioButton_monitor_bp = QRadioButton("Bio Production")
        radioButton_monitor_by = QRadioButton("Biogas Yueld")
        radioButton_monitor_vsr = QRadioButton("VSRem")
        radioButton_monitor_vfa = QRadioButton("VFA")
        radioButton_monitor_alk = QRadioButton("Alk")
        radioButton_monitor_va = QRadioButton("VFA/Alk")
        outputGroupBox = QGroupBox("출력 그래프 선택")
        radioButton_monitor_prdct = QRadioButton("예측")
        radioButton_monitor_rcnt = QRadioButton("추세")
        pushButton_monitor_plot = QPushButton("출력")

        btnValueLayout = QHBoxLayout()
        btnValueLayout.addWidget(radioButton_monitor_bp)
        btnValueLayout.addWidget(radioButton_monitor_by)
        btnValueLayout.addWidget(radioButton_monitor_vsr)
        btnValueLayout.addWidget(radioButton_monitor_vfa)
        btnValueLayout.addWidget(radioButton_monitor_alk)
        btnValueLayout.addWidget(radioButton_monitor_va)
        valueGroupBox.setLayout(btnValueLayout)

        btnOutputLayout = QHBoxLayout()
        btnOutputLayout.addWidget(radioButton_monitor_prdct)
        btnOutputLayout.addWidget(radioButton_monitor_rcnt)
        outputGroupBox.setLayout(btnOutputLayout)
        

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(valueGroupBox)
        inputLayout.addWidget(outputGroupBox)
        inputLayout.addWidget(pushButton_monitor_plot)

        outputLayout = QHBoxLayout()       
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        outputLayout.addWidget(self.canvas)
     
        layout = QVBoxLayout()
        layout.addLayout(inputLayout)
        layout.addLayout(outputLayout)
     
        self.setLayout(layout)               

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
            
         
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MonitorWindow()
    sys.exit(app.exec_())
