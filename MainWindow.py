import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, \
                            QGridLayout, QHBoxLayout, QTableWidget, QHeaderView, \
                            QAbstractItemView, QTableWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QImage, QPixmap

from Configure import Configure


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.video_1 = VideoItem()
        self.video_2 = VideoItem()
        self.video_3 = VideoItem()
        self.video_4 = VideoItem()

        video_layout = QGridLayout()
        video_layout.addWidget(self.video_1, 0, 0)
        video_layout.addWidget(self.video_2, 0, 1)
        video_layout.addWidget(self.video_3, 1, 0)
        video_layout.addWidget(self.video_4, 1, 1)

        self.up_pushbutton = QPushButton()
        self.down_pushbutton = QPushButton()
        self.left_pushbutton = QPushButton()
        self.right_pushbutton = QPushButton()

        self.up_pushbutton.setFixedSize(40, 40)
        self.down_pushbutton.setFixedSize(40, 40)
        self.left_pushbutton.setFixedSize(40, 40)
        self.right_pushbutton.setFixedSize(40, 40)

        self.up_pushbutton.setObjectName('up')
        self.down_pushbutton.setObjectName('down')
        self.left_pushbutton.setObjectName('left')
        self.right_pushbutton.setObjectName('right')


        direction_layout = QGridLayout()
        direction_layout.addWidget(self.up_pushbutton, 0, 1)
        direction_layout.addWidget(self.down_pushbutton, 2, 1)
        direction_layout.addWidget(self.left_pushbutton, 1, 0)
        direction_layout.addWidget(self.right_pushbutton, 1, 2)

        self.change_focus = FunctionItem('焦距')
        self.change_aperture = FunctionItem('光圈')

        control_layout = QVBoxLayout()
        control_layout.addLayout(direction_layout)
        control_layout.addLayout(self.change_focus)
        control_layout.addLayout(self.change_aperture)

        self.table_widget = MyTableWidget()

        main_layout = QHBoxLayout()
        main_layout.addLayout(video_layout)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.table_widget)
        main_layout.setStretchFactor(video_layout, 5)
        main_layout.setStretchFactor(control_layout, 1)

        self.setLayout(main_layout)

        self.up_pushbutton.clicked.connect(self.upwards)
        self.down_pushbutton.clicked.connect(self.downwards)
        self.left_pushbutton.clicked.connect(self.leftwards)
        self.right_pushbutton.clicked.connect(self.rightwards)

        self.change_focus.up_pushbutton.clicked.connect(self.add_focus)
        self.change_focus.down_pushbutton.clicked.connect(self.sub_focus)
        self.change_aperture.up_pushbutton.clicked.connect(self.add_aperture)
        self.change_aperture.down_pushbutton.clicked.connect(self.sub_aperture)

        self.video_1.pos_signal.connect(self.set_pos)
        self.video_2.pos_signal.connect(self.set_pos)
        self.video_3.pos_signal.connect(self.set_pos)
        self.video_4.pos_signal.connect(self.set_pos)

    # 向上
    def upwards(self):
        print('upwards')

    # 向下
    def downwards(self):
        print('downwards')

    # 向左
    def leftwards(self):
        print('leftwards')

    # 向右
    def rightwards(self):
        print('rightwards')

    # 增大焦距
    def add_focus(self):
        print('add_focus')

    # 减小焦距
    def sub_focus(self):
        print('sub_focus')

    # 增大光圈
    def add_aperture(self):
        print('add_aperture')
    
    # 减小光圈
    def sub_aperture(self):
        print('sub_aperture')

    def set_pos(self, x, y):
        self.table_widget.set_pos(x, y)


class VideoItem(QLabel):
    pos_signal = pyqtSignal(int, int)
    def __init__(self):
        super(VideoItem, self).__init__()
        self.setMinimumSize(500, 300)
        self.push_button = QPushButton('')
        self.push_button.setFixedSize(40, 40)
        self.configure = Configure()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.push_button)
        main_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.push_button.clicked.connect(self.configure.show)

        self.setStyleSheet('background-color: gray')

        self.timer_camera = QTimer(self)
        self.cap = cv2.VideoCapture('./test/test.3gp')
        self.timer_camera.timeout.connect(self.show_pic)
        self.timer_camera.start(10)

    def show_pic(self):
        success, frame = self.cap.read()
        if success:
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = self.handle_image(QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888))
            self.setPixmap(QPixmap.fromImage(image).scaled(self.size()))
            self.timer_camera.start(10)

    # 处理视频帧
    def handle_image(self, image):
        return image

    def mousePressEvent(self, event):
        self.pos_signal.emit(event.pos().x(), event.pos().y())


class FunctionItem(QVBoxLayout):
    def __init__(self, text):
        super(FunctionItem, self).__init__()

        self.up_pushbutton = QPushButton()
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignHCenter)
        self.down_pushbutton = QPushButton()
        self.up_pushbutton.setFixedSize(40, 40)
        self.down_pushbutton.setFixedSize(40, 40)
        self.up_pushbutton.setObjectName('fun_up')
        self.down_pushbutton.setObjectName('fun_down')

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        self.addWidget(self.up_pushbutton)
        self.addWidget(self.label)
        self.addWidget(self.down_pushbutton)
        self.setAlignment(Qt.AlignCenter)


class MyTableWidget(QWidget):
    def __init__(self):
        super(MyTableWidget, self).__init__()
        self.table_widget = QTableWidget(5, 5)
        self.add_pushbutton = QPushButton(clicked=self.add_row)
        self.remove_pushbutton = QPushButton(clicked=self.remove_row)
        self.start_pushbutton = QPushButton('start', clicked=self.start_calculate)
        self.add_pushbutton.setObjectName('add')
        self.remove_pushbutton.setObjectName('remove')

        self.table_widget.setMinimumWidth(400)
        self.table_widget.setHorizontalHeaderLabels(['x', 'y', 'α', 'β', 'get'])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.add_pushbutton)
        h_layout.addStretch()
        h_layout.addWidget(self.remove_pushbutton)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_widget)
        main_layout.addLayout(h_layout)
        main_layout.addWidget(self.start_pushbutton)

        self.setLayout(main_layout)

    def add_row(self):
        self.table_widget.setRowCount(self.table_widget.rowCount() + 1)

    def remove_row(self):
        self.table_widget.removeRow(self.table_widget.currentRow())

    def set_pos(self, x, y):
        if self.table_widget.currentRow() == -1:
            for i in range(self.table_widget.rowCount()):
                if self.table_widget.item(i, 0) is None:
                    self.table_widget.setItem(i, 0, QTableWidgetItem(str(x)))
                    self.table_widget.setItem(i, 1, QTableWidgetItem(str(y)))
                    get_pushbutton = QPushButton('get', clicked=self.get_alpha_beta)
                    # get_pushbutton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                    get_pushbutton.setFixedWidth(65)
                    self.table_widget.setCellWidget(i, 4, get_pushbutton)
                    break
        else:
            current_row = self.table_widget.currentRow()
            self.table_widget.setItem(current_row, 0, QTableWidgetItem(str(x)))
            self.table_widget.setItem(current_row, 1, QTableWidgetItem(str(y)))
            self.table_widget.setCellWidget(current_row, 4, QPushButton('get', clicked=self.get_alpha_beta))

    def get_alpha_beta(self):
        sender_frame_geometry = self.sender()
        current_row = self.table_widget.indexAt(QPoint(sender_frame_geometry.x(), sender_frame_geometry.y())).row()
        x = int(self.table_widget.item(current_row, 0).text())
        y = int(self.table_widget.item(current_row, 1).text())
        self.table_widget.setItem(current_row, 2, QTableWidgetItem(str(x + 1)))
        self.table_widget.setItem(current_row, 3, QTableWidgetItem(str(y + 2)))

    def start_calculate(self):
        for i in range(self.table_widget.rowCount()):
             if not self.table_widget.item(i, 0) is None:
                alpha = self.table_widget.item(i, 0).text()
                beta = self.table_widget.item(i, 1).text()
                print('alpha:', alpha, 'beta:', beta)
                


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    qss = open('./source.qss').read()
    app.setStyleSheet(qss)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())

