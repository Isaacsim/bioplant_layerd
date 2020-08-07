import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd
from monitor import MONITOR_INPUT_LIST

def setRawdata(raw_data):
    
    return raw_data

def get():
    return setRawdata.raw_data

class RawdataWindow(QDialog):

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
            self.raw_data = pd.read_csv('raw_data.csv')
            self.rawdataValidation()

    def importFromPath(self):        
        fname = QFileDialog.getOpenFileName(self)        
        if fname[0].endswith('.csv') == False:
            self.rawdata_label_2.setText("CSV 확장자 파일만 가져올 수 있습니다.")
            self.rawdata_vali = False
            return
        self.raw_data = pd.read_csv(fname[0])
        self.rawdataValidation()

    def exportRawdata(self):
        if self.rawdata_vali is True:
            self.raw_data.to_csv("raw_data_exported.csv")
            self.rawdata_label_2.setText("루트폴더에 raw_data_exported.csv로 저장되었습니다.")
        else:
            self.rawdata_label_2.setText("추출할 데이터가 없습니다.")

    def appendRawdata(self):
        if self.rawdata_vali is False:
            self.rawdata_label_2.setText("입력할 데이터 목록이 없습니다.")
        pass

    def rawdataValidation(self):
        for i in range(0,len(MONITOR_INPUT_LIST)):
            if self.raw_data.columns[i+2] != MONITOR_INPUT_LIST[i]:
                self.rawdata_label_2.setText("csv 파일의 범주가 맞지 않습니다. 지정된 범례로 구성된 데이터인지 확인하십시오.")
                self.rawdata_vali = False
                return
        self.rawdata_label_2.setText("가져오기 성공")
        self.rawdata_vali = True        
        setRawdata(self.raw_data)
                
class setRawdataFromRoot(QDialog) :

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):        
        fname = QFileDialog.getOpenFileName(self)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RawdataWindow()
    window.show()
    app.exec_()