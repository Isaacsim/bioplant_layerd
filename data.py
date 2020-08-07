import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd
from settings import *

raw_data = []

def getRawData():
    global raw_data
    return raw_data

class DataWindow(QWidget):    
    def __init__(self):
        super().__init__()        
        self.initUI()

    def initUI(self):
        self.rawdata_label_1 = QLabel("분석에 사용될 Raw data를 가져오십시오.")
        self.rawdata_push_1 = QPushButton("루트폴더에서 가져오기")
        self.rawdata_push_2 = QPushButton("지정루트에서 가져오기")
        self.rawdata_label_2 = QLabel()
        self.rawdata_push_3 = QPushButton("분석중인 데이터 추출")
        self.rawdata_push_4 = QPushButton("신규데이터 추가")

        layout = QVBoxLayout()
        layout.addWidget(self.rawdata_label_1)
        layout.addWidget(self.rawdata_push_1)
        layout.addWidget(self.rawdata_push_2)
        layout.addWidget(self.rawdata_label_2)
        layout.addWidget(self.rawdata_push_3)
        layout.addWidget(self.rawdata_push_4)

        self.setLayout(layout)
        self.rawdata_push_1.clicked.connect(self.importFromRoot)
        self.rawdata_push_2.clicked.connect(self.importFromPath)
        self.rawdata_push_3.clicked.connect(self.exportRawdata)
        self.rawdata_push_4.clicked.connect(self.appendRawdata)

        self.rawdata_vali = False

    def importFromRoot(self):
        if os.path.exists('raw_data.csv'):
            data = pd.read_csv('raw_data.csv')
            if self.rawdataValidation(data) == True:
                global raw_data
                raw_data = data

    def importFromPath(self):        
        fname = QFileDialog.getOpenFileName(self)        
        if fname[0].endswith('.csv') == False:
            self.rawdata_label_2.setText("CSV 확장자 파일만 가져올 수 있습니다.")
            self.rawdata_vali = False
            return
        data = pd.read_csv(fname[0])
        if self.rawdataValidation(data) == True:
            global raw_data
            raw_data = data

    def exportRawdata(self):
        global raw_data
        if len(raw_data) == 0:
            self.rawdata_label_2.setText("추출할 데이터가 없습니다.")
            return 0
        else:
            raw_data.to_csv("raw_data_exported.csv", index=False)
        self.rawdata_label_2.setText("raw_data_exported.csv로 저장하였습니다.")

    def appendRawdata(self):
        if self.rawdata_vali is False:
            self.rawdata_label_2.setText("입력할 데이터 목록이 없습니다.")
        pass

    def rawdataValidation(self, data):
        for i in range(0,len(MONITOR_INPUT_LIST)):
            if data.columns[i+2] != MONITOR_INPUT_LIST[i]:
                self.rawdata_label_2.setText("csv 파일의 범주가 맞지 않습니다. 지정된 범례로 구성된 데이터인지 확인하십시오.")
                return False
        self.rawdata_label_2.setText("가져오기 성공")
        return True
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataWindow()
    window.show()
    app.exec_()