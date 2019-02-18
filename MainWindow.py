import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, \
							QGridLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
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

		right_layout = QVBoxLayout()
		right_layout.addLayout(direction_layout)
		right_layout.addLayout(self.change_focus)
		right_layout.addLayout(self.change_aperture)

		main_layout = QHBoxLayout()
		main_layout.addLayout(video_layout)
		main_layout.addLayout(right_layout)
		main_layout.setStretchFactor(video_layout, 5)
		main_layout.setStretchFactor(right_layout, 1)

		self.setLayout(main_layout)

		self.up_pushbutton.clicked.connect(self.upwards)
		self.down_pushbutton.clicked.connect(self.downwards)
		self.left_pushbutton.clicked.connect(self.leftwards)
		self.right_pushbutton.clicked.connect(self.rightwards)

		self.change_focus.up_pushbutton.clicked.connect(self.add_focus)
		self.change_focus.down_pushbutton.clicked.connect(self.sub_focus)
		self.change_aperture.up_pushbutton.clicked.connect(self.add_aperture)
		self.change_aperture.down_pushbutton.clicked.connect(self.sub_aperture)

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


class VideoItem(QLabel):
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
		self.cap = cv2.VideoCapture('./test/test.avi')
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


if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	qss = open('./source.qss').read()
	app.setStyleSheet(qss)
	mainwindow = MainWindow()
	mainwindow.show()
	sys.exit(app.exec_())

