from PyQt5 import QtCore
import pandas as pd
class PdTable(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def headerData(self, col, orientation, role):

        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if self._data.columns[col] == "Time":
                return "Date" #결함7
            return self._data.columns[col]
        return None

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(str(
                    round(self._data.values[index.row()][index.column()], 3)))
        return QtCore.QVariant()