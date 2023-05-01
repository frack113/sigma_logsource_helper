from PyQt6 import QtWidgets, uic
import sys
from ruamel.yaml import YAML

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.button_load = self.findChild(QtWidgets.QPushButton, 'Button_load') # Find the button
        self.button_load.clicked.connect(self.load) # Remember to pass the definition/method, not the return value!

        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.explicit_start = False
        self.yaml.preserve_quotes = True
        self.yaml.width = 2000
        self.yaml.indent(mapping=4, sequence=4, offset=4)
        self.yaml_data = {}

        self.show()


    def load(self):
        with open('logsource.yml', encoding="UTF-8") as file_in:
            self.yaml_data = self.yaml.load(file_in)

        list_q1 = self.findChild(QtWidgets.QListView, 'listView_1')
        for uuid in self.yaml_data['question_general']:
            QtWidgets.QListWidgetItem(str(self.yaml_data['question_general'][uuid]['ask']),list_q1)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()
