from PyQt5.QtWidgets import QWidget,QHeaderView, QTableWidgetItem, QTableWidget, QCheckBox, QHBoxLayout
from PyQt5 import uic
from PyQt5.Qt import Qt, QPalette
from PyQt5.QtGui import QFont
import csv
DATA_PATH = './csv_data'


class WorkArea(QWidget):
    def __init__(self, parent= None, ch_file= None):
        super(WorkArea, self).__init__(parent)
        uic.loadUi("ui\work_area.ui", self)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.WindowModal)

        self.work_table.setColumnWidth(0, 300)
        self.work_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.work_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.work_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        if ch_file is not None:
            self.read_csv_data()
        else:
            self.insert_data_to_table(0, 0,'')
            self.insert_chekbox_to_table(0, 1, 0)
            self.insert_chekbox_to_table(0, 2, 0)
            self.insert_data_to_table(0, 3, '')

    def keyPressEvent(self, ev):
        if ev.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.add_new_row()

        if ev.key() == Qt.Key_Delete:
            self.work_table.removeRow(self.work_table.currentRow())

    def add_new_row(self):
        row_count = self.work_table.rowCount() + 1
        self.work_table.setRowCount(row_count)
        self.insert_data_to_table(row_count, 0, '')
        self.insert_chekbox_to_table(row_count, 1, 0)
        self.insert_chekbox_to_table(row_count, 2, 0)
        self.insert_data_to_table(row_count, 3, '')

    def read_csv_data(self):
        with open('{}/{}'.format(DATA_PATH, self.name_data),'r', encoding='utf-8') as f:
            fields = ['Doing', 'PASS_ch', 'FAIL_ch', 'Comment']
            reader = csv.DictReader(f, fields, delimiter=',')
            csv_l = []
            for csv_row in reader:
                csv_l.append(csv_row)

            self.work_table.setRowCount(len(csv_l))
            row_index = 0
            for row in csv_l:
                self.insert_data_to_table(row_index, 0, row['Doing'])
                self.insert_chekbox_to_table(row_index, 1, int(row['PASS_ch']))
                self.insert_chekbox_to_table(row_index, 2, int(row['FAIL_ch']))
                self.insert_data_to_table(row_index, 3, row['Comment'])
                row_index += 1

    def insert_data_to_table(self, row, column, text):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFont(QFont('Tahoma', 10))
        self.work_table.setItem(row, column, item)

    def onStateChanged(self):
        ch_sender = self.sender()
        row, column = str(ch_sender.objectName()).split('-')
        pl = QPalette()

        if ch_sender.checkState() == Qt.Checked:
            if column == '1':
                pl.setColor(QPalette.Background, Qt.green)
                w_item = self.work_table.cellWidget(int(row), int(column))
                w_item.setAutoFillBackground(True)
                w_item.setPalette(pl)

                pl.setColor(QPalette.Background, Qt.white)
                w_another_ch = self.work_table.cellWidget(int(row), 2)
                child_ch = w_another_ch.findChild(QCheckBox)
                child_ch.setCheckState(Qt.Unchecked)
                w_another_ch.setAutoFillBackground(True)
                w_another_ch.setPalette(pl)
            else:
                pl.setColor(QPalette.Background, Qt.red)
                w_item = self.work_table.cellWidget(int(row), int(column))
                w_item.setAutoFillBackground(True)
                w_item.setPalette(pl)

                pl.setColor(QPalette.Background, Qt.white)
                w_another_ch = self.work_table.cellWidget(int(row), 1)
                child_ch = w_another_ch.findChild(QCheckBox)
                child_ch.setCheckState(Qt.Unchecked)
                w_another_ch.setAutoFillBackground(True)
                w_another_ch.setPalette(pl)
        else:
            pl.setColor(QPalette.Background, Qt.white)
            w_item = self.work_table.cellWidget(int(row), int(column))
            w_item.setAutoFillBackground(True)
            w_item.setPalette(pl)
        pass

    def insert_chekbox_to_table(self, row, column, status):
        cell_widget = QWidget()
        chk_bx = QCheckBox()
        chk_bx.setObjectName('{}-{}'.format(row, column))
        lay_out = QHBoxLayout(cell_widget)
        lay_out.addWidget(chk_bx)
        lay_out.setAlignment(Qt.AlignCenter)
        lay_out.setContentsMargins(0, 0, 0, 0)
        cell_widget.setLayout(lay_out)
        pl = QPalette()

        if status:
            if column == 1:
                pl.setColor(QPalette.Background, Qt.green)
            else:
                pl.setColor(QPalette.Background, Qt.red)

            chk_bx.setCheckState(Qt.Checked)
            cell_widget.setAutoFillBackground(True)
            cell_widget.setPalette(pl)
        else:
            chk_bx.setCheckState(Qt.Unchecked)
        chk_bx.clicked.connect(self.onStateChanged)
        self.work_table.setFocusPolicy(Qt.NoFocus)
        self.work_table.setCellWidget(row, column, cell_widget)




