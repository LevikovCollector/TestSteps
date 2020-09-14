from PyQt5.QtWidgets import QMainWindow, QApplication, QStyleFactory, QListWidget
from PyQt5 import uic
import sys, os, time
from work_area import WorkArea

DATA_PATH = './csv_data'

class MainForm(QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        uic.loadUi("ui\Main.ui", self)

        self.create_steps.clicked.connect(self.open_work_area)
        self.delete_file_steps.clicked.connect(self.delete_file)
        self.create_test_list()

    def create_test_list(self):
        all_files = os.listdir(DATA_PATH)
        self.list_files.addItems(all_files)

    def delete_file(self):
        item = self.list_files.currentItem()
        os.remove('{}/{}'.format(DATA_PATH, item.text()))
        self.list_files.clear()
        self.create_test_list()

    def open_work_area(self):
        wa = WorkArea(self)
        wa.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    main_form = MainForm()
    main_form.show()
    sys.exit(app.exec_())