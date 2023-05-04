from PyQt6 import QtWidgets, uic
import sys
from ruamel.yaml import YAML

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.list_q1 = self.findChild(QtWidgets.QListWidget, 'list_q1')
        self.dictq1 ={}
        self.button_v1 = self.findChild(QtWidgets.QPushButton, 'valide_1')
        self.button_v1.clicked.connect(self.itemClicked_event_v1)

        self.list_q2 = self.findChild(QtWidgets.QListWidget, 'list_q2')
        self.dictq2 = {}
        self.button_v2 = self.findChild(QtWidgets.QPushButton, 'valide_2')
        self.button_v2.clicked.connect(self.itemClicked_event_v2)

        self.list_q3 = self.findChild(QtWidgets.QListWidget, 'list_q3')
        self.dictq3 = {}
        self.button_v3 = self.findChild(QtWidgets.QPushButton, 'valide_3')
        self.button_v3.clicked.connect(self.itemClicked_event_v3)
       
        self.table_log = self.findChild(QtWidgets.QTableWidget, 'tableWidget')

        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.explicit_start = False
        self.yaml.preserve_quotes = True
        self.yaml.width = 2000
        self.yaml.indent(mapping=4, sequence=4, offset=4)
        self.yaml_data = {}

        self.load()
        self.show()
    
    def load(self):
        with open('logsource.yml', encoding="UTF-8") as file_in:
            self.yaml_data = self.yaml.load(file_in)

        self.list_q1.clear()
        i = 0 # dirty
        for uuid in self.yaml_data['question_general']:
            self.list_q1.addItem(self.yaml_data['question_general'][uuid]['ask'])
            self.dictq1[i]=uuid
            i += 1

    def itemClicked_event_v1(self):
        self.list_q2.clear()
        self.dictq2 = {}
        i = 0
        for item in self.list_q1.selectedItems():
            row = self.list_q1.row(item)
            for next_uuid in self.yaml_data['question_general'][self.dictq1[row]]['uuid_ref']:
                self.dictq2[i] = next_uuid
                i += 1
                self.list_q2.addItem(self.yaml_data['questions_type'][next_uuid]['ask'])

    def itemClicked_event_v2(self):
        self.list_q3.clear()
        self.dictq3 = {}
        i = 0
        for item in self.list_q2.selectedItems():
            row = self.list_q2.row(item)
            for next_uuid in self.yaml_data['questions_type'][self.dictq2[row]]['uuid_ref']:
                self.dictq3[i] = next_uuid
                i += 1
                self.list_q3.addItem(self.yaml_data['questions_logsources'][next_uuid]['ask'])

    def itemClicked_event_v3(self):
        self.table_log.setRowCount(0) #clean ?
        data =[('product','category','service')]
        for item in self.list_q3.selectedItems():
            q3_row = self.list_q3.row(item)
            for next_uuid in self.yaml_data['questions_logsources'][self.dictq3[q3_row]]['uuid_ref']:
                row_data=(self.yaml_data['logsources'][next_uuid]['product'],
                    self.yaml_data['logsources'][next_uuid]['category'],
                    self.yaml_data['logsources'][next_uuid]['service'])
                data.append(row_data)
        
        numrows = len(data)
        numcols = len(data[0])
        self.table_log.setColumnCount(numcols)
        self.table_log.setRowCount(numrows)

        for row in range(numrows):
            for column in range(numcols):
                 self.table_log.setItem(row, column, QtWidgets.QTableWidgetItem((data[row][column])))

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()
