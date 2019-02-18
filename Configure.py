# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
                             QGridLayout, QMessageBox, QSizePolicy, QFormLayout)
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QIcon

class Configure(QWidget):

    def __init__(self):
        super(Configure, self).__init__()
        self.setWindowTitle('Setting')
        self.resize(500, 250)
        
        self.ip_line = QLineEdit()
        self.user_line = QLineEdit()
        self.pass_line = QLineEdit()
        self.ok_button = QPushButton('确定')
        self.cancel_button = QPushButton('取消')
        
        main_layout = QFormLayout()
        main_layout.addRow(QLabel('ip:'), self.ip_line)
        main_layout.addRow(QLabel('user:'), self.user_line)
        main_layout.addRow(QLabel('pass:'), self.pass_line)
        main_layout.addRow(self.ok_button, self.cancel_button)

        self.setLayout(main_layout)

        self.ok_button.clicked.connect(self.test_slot)

    def test_slot(self):
    	ip = self.ip_line.text()
    	user = self.user_line.text()
    	password = self.pass_line.text()
    	print('ip:', ip, '\nuser:', user, '\npassword:', password)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    config = Configure()
    config.show()
    sys.exit(app.exec_())
