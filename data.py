import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDoubleValidator, QIntValidator
import pandas as pd
from settings import MONITOR_INPUT_LIST
from pdtable import PdTable
from settings import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from predict import PredictWindow

CSV_COLUMN_LIST = ["Time","OLR","VFA","Alk","VFA/Alk","Biogas Production","Biogas Yield","VSRem"]
raw_data = []
raw_data_appended = []


def getRawData():
    global raw_data
    return raw_data


class DataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.rawdata_table_1 = QTableView()
        self.rawdata_label_1 = QLabel("분석에 사용될 Raw data를 가져오십시오.")
        self.rawdata_push_1 = QPushButton("루트폴더에서 가져오기")
        self.rawdata_push_2 = QPushButton("지정루트에서 가져오기")
        self.rawdata_label_2 = QLabel()
        self.rawdata_push_3 = QPushButton("분석중인 데이터 추출")
        self.rawdata_push_4 = QPushButton("신규데이터 추가")

        self.leftLayout = QVBoxLayout()
        self.leftLayout.addWidget(self.rawdata_table_1)

        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.rawdata_label_1)
        self.rightLayout.addWidget(self.rawdata_push_1)
        self.rightLayout.addWidget(self.rawdata_push_2)
        self.rightLayout.addWidget(self.rawdata_label_2)
        self.rightLayout.addWidget(self.rawdata_push_3)
        self.rightLayout.addWidget(self.rawdata_push_4)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.leftLayout)
        self.layout.addLayout(self.rightLayout)
        self.setLayout(self.layout)
        self.rawdata_push_1.clicked.connect(self.importFromRoot)
        self.rawdata_push_2.clicked.connect(self.importFromPath)
        self.rawdata_push_3.clicked.connect(self.exportRawdata)
        self.rawdata_push_4.clicked.connect(self.appendRawdata)
        
        self.rawdata_vali = False


    def importFromRoot(self):
        if os.path.exists("raw_data.csv"):
            data = pd.read_csv("raw_data.csv")
            if self.rawdataValidation(data) == True:
                global raw_data
                raw_data = data
                self.setDataTable(raw_data)

    def importFromPath(self):
        fname = QFileDialog.getOpenFileName(self)
        if fname[0].endswith(".csv") == False:
            self.rawdata_label_2.setText(
                "CSV 확장자 파일만 가져올 수 있습니다."
            )
            self.rawdata_vali = False
            return
        data = pd.read_csv(fname[0])
        if self.rawdataValidation(data) == True:
            global raw_data
            raw_data = data
            self.setDataTable(raw_data)

    def exportRawdata(self):
        global raw_data
        if len(raw_data) == 0:
            self.rawdata_label_2.setText("추출할 데이터가 없습니다.")
            return 0
        else:
            raw_data.to_csv("raw_data_exported.csv", index=False)
        self.rawdata_label_2.setText("raw_data_exported.csv로 저장하였습니다.")

    def appendRawdata(self):
        global raw_data
        if len(raw_data) == 0:
            self.rawdata_label_2.setText("입력할 데이터 목록이 없습니다.")            
        dlg = ImportWindow()
        dlg.exec_()

    def rawdataValidation(self, data):
        for i in range(0, len(MONITOR_INPUT_LIST)):
            if data.columns[i + 2] != MONITOR_INPUT_LIST[i]:
                self.rawdata_label_2.setText(
                    "csv 파일의 범주가 맞지 않습니다."
                )
                return False
        self.rawdata_label_2.setText("가져오기 성공")
        return True

    def setDataTable(self, raw_data):
        model = PdTable(raw_data)
        self.rawdata_table_1.setModel(model)


class ImportWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.import_spins = []
        self.import_labels_1 = []
        self.import_labels_2 = []        
        for i in range(0, len(CSV_COLUMN_LIST)):
            if i == 0:
                self.import_spins.append(QSpinBox())
                self.import_spins[i].setRange(int(raw_data.tail(1)["Time"])+1, 9999999)
                self.import_labels_1.append(QLabel(CSV_COLUMN_LIST[i]))
                self.import_labels_2.append(QLabel(str(int(raw_data.tail(1)[CSV_COLUMN_LIST[i]]))))
            else:
                self.import_spins.append(QDoubleSpinBox())
                self.import_spins[i].setRange(0, 9999999)
                self.import_labels_1.append(QLabel(CSV_COLUMN_LIST[i]))
                self.import_labels_2.append(QLabel(str(round(float(raw_data.tail(1)[CSV_COLUMN_LIST[i]]), 2))))     

        self.import_push_1 = QPushButton("데이터 유효성 검사")
        self.import_label_1 = QLabel("입력 데이터")
        self.import_label_2 = QLabel("가장 최근 데이터")
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.import_label_1, 0, 2)        
        self.layout.addWidget(self.import_label_2, 0, 1)
        for i in range(0, len(CSV_COLUMN_LIST)):
            self.layout.addWidget(self.import_spins[i], i + 1, 2)
            self.layout.addWidget(self.import_labels_1[i], i + 1, 0)
            self.layout.addWidget(self.import_labels_2[i], i + 1, 1)
        self.layout.addWidget(self.import_push_1, len(CSV_COLUMN_LIST)+2, 2)

        self.setLayout(self.layout)

        self.import_push_1.clicked.connect(self.valiData)

    def valiData(self):
        self.vali_label_1 = QLabel("유효성")
        self.vali_label_2 = QLabel("입력여부")
        self.vali_labels_1 = []
        self.vali_checks_1 = []
        self.vali_percents_1 = []
        self.vali_push_1 = QPushButton("데이터 입력")

        for i in range(0, len(CSV_COLUMN_LIST)):
            percent = round(float(raw_data.tail(1)[CSV_COLUMN_LIST[i]] / raw_data.tail(LEARNING_RANGE)[CSV_COLUMN_LIST[i]].mean()), 3)
            self.vali_percents_1.append(percent)            
            self.vali_labels_1.append(QLineEdit())            
            self.vali_checks_1.append(QCheckBox())
            
            imp_value = round(self.import_spins[i].value() / raw_data.tail(LEARNING_RANGE)[CSV_COLUMN_LIST[i]].mean(), 3)
            check = abs(imp_value - self.vali_percents_1[i])

            if check < 0.25:                
                self.vali_labels_1[i].setText("합격")
                self.vali_checks_1[i].setCheckState(2)
                print(self.vali_checks_1[i].checkState())
            else:                
                self.vali_labels_1[i].setText("불합")   

        self.layout.addWidget(self.vali_label_1, 0, 3)
        self.layout.addWidget(self.vali_label_2, 0, 4)
        for i in range(0, len(CSV_COLUMN_LIST)):
            self.layout.addWidget(self.vali_labels_1[i], i + 1, 3)
            self.layout.addWidget(self.vali_checks_1[i], i + 1, 4)
        self.layout.addWidget(self.vali_push_1, len(CSV_COLUMN_LIST) + 2, 4)
        self.setLayout(self.layout)        

        self.vali_push_1.clicked.connect(self.importCheck)

        self.infoValiData()

    def importCheck(self):
        self.stateCheck()
        if self.prog == True:
            self.importRow()
            self.close()
        print(self.prog)
        

    def stateCheck(self):
        self.passedRow = []
        self.importedRow = []
        self.prog = False
        for i in range(0, len(CSV_COLUMN_LIST)):
            if self.vali_labels_1[i].text() == "불합" and self.vali_checks_1[i].checkState() == 2:
                for j in range(0, len(CSV_COLUMN_LIST)):
                    if self.vali_labels_1[j].text() == "합격":
                        self.passedRow.append(CSV_COLUMN_LIST[j])
                    if self.vali_checks_1[j].checkState() == 2:
                        self.importedRow.append(CSV_COLUMN_LIST[j])                    
                info_m = f"유효성 합격 데이터 = {str(self.passedRow)} \n 입력하려는 데이터 = {str(self.importedRow)} \n 유효성 결과를 무시하고 입력하시겠습니까?"
                question = QMessageBox.question(self, "주의", info_m)
                if question == QMessageBox.Yes:
                    self.prog = True            
                    return                    
                else:
                    return
        
        self.prog = True
        return

    def importRow(self):
        
        global raw_data
        a_row = pd.DataFrame()
        a_row = a_row.append(raw_data.iloc[-1], sort=False)
        for i in range(0, len(CSV_COLUMN_LIST)):
            if self.vali_checks_1[i].checkState() == 2:
                a_row.iloc[-1][CSV_COLUMN_LIST[i]] = self.import_spins[i].value()

        print(a_row)
        global raw_data_appended
        raw_data_appended = []
        raw_data_appended = raw_data.append(a_row)
        print(raw_data_appended)

        dlg = instantPlotWindow()
        dlg.exec_()
            
    def setMonitorPredicted(self, input_name):
        raw_data = getRawData()
        if len(raw_data) == 0:
            self.warnRawData()
            return
        PredictWindow(self.fig, input_name, raw_data)
        self.canvas.draw()

    def infoValiData(self):
        QMessageBox.information(self, "유효성 검사 완료", "데이터 유효범위 안에 없는 항목은 체크해제됩니다. \n 입력여부를 체크한 항목만 입력됩니다. \n 체크해제된 항목은 가장 최근 데이터값을 가져옵니다.")


        


class instantPlotWindow(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.appendToCSV()

    def initUI(self):

        self.instplot_push_1 = QPushButton("확인")
        self.instplot_label_1 = QLabel()
        self.instplot_label_1.setText(f"데이터 추가 완료 Biogas production의 예측범위의 변화를 비교하십시오. \n 나머지 parameter는 monitor탭에서 확인 가능")

        self.outputLayout = QHBoxLayout()
        self.fig_1 = plt.Figure()
        self.canvas_1 = FigureCanvas(self.fig_1)
        self.fig_2 = plt.Figure()
        self.canvas_2 = FigureCanvas(self.fig_2)
        self.outputLayout.addWidget(self.canvas_1)
        self.outputLayout.addWidget(self.canvas_2)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.instplot_label_1)
        self.buttonLayout.addWidget(self.instplot_push_1)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.outputLayout)
        self.layout.addLayout(self.buttonLayout)

        self.setLayout(self.layout)

        PredictWindow(self.fig_1, "Biogas Production", raw_data)
        self.canvas_1.draw()
        PredictWindow(self.fig_2, "Biogas Production", raw_data_appended)
        self.canvas_2.draw()

        self.instplot_push_1.clicked.connect(self.close)



    def appendToCSV(self):
        raw_data_appended.to_csv("raw_data.csv", index=False)
        global raw_data
        raw_data = raw_data_appended


    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataWindow()
    window.show()
    app.exec_()