import ctypes
import inspect
import cv2
import pandas as pd
from PyQt5 import  QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from FaceRecognition.utils.getFiles import *
from FaceRecognition.ui.informationWindow import informationWindow
from FaceRecognition.utils.mythread import MyThread
from FaceRecognition.utils.getFiles import GetFiles
from FaceRecognition.algorithm import face
import glob

import time as tim

import xml.dom.minidom as xmldom

# 打开并读取文件

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        self.set_ui()
        self.slot_init()
        self.button_list = []

        self.new_window = None

    def set_ui(self):
        self.setWindowTitle('人脸识别签到系统  作者：qrz')
        self.setGeometry(100, 100, 1500, 900)
        # 创建stacked_widget并设置为窗口的中心部件
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        '''页面1'''
        page1 = QWidget()

        self.button_page1 = QPushButton("首页")
        self.button_page1.setGeometry(10, 10, 100, 50)
        self.button_page1.setCheckable(True)
        self.button_page1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_page1.setParent(self)

        self.label_show1 = QtWidgets.QLabel(page1)
        self.label_show1.setGeometry(10, 105, 1400, 900)
        self.label_show1.setAutoFillBackground(True)
        self.label_show1.setLineWidth(1)
        # self.label_show1.setParent(self)
        self.label_show1.setAlignment(Qt.AlignCenter)
        self.label_show1.setStyleSheet("QLabel {font-size: 24px; \
        background-color:#F5F5F5; \
        padding: 6px; \
        border: 1px solid black; \
        }")

        self.label_show2 = QtWidgets.QLabel(page1)
        self.label_show2.setGeometry(1420, 105, 250, 300)
        self.label_show2.setAutoFillBackground(True)
        self.label_show2.setLineWidth(1)
        # self.label_show1.setParent(self)
        self.label_show2.setAlignment(Qt.AlignCenter)
        self.label_show2.setStyleSheet("QLabel {font-size: 24px; \
                background-color:#F5F5F5; \
                padding: 6px; \
                border: 1px solid black; \
                }")

        # self.label_show2.setFont(font2)

        self.label = QLabel("姓名:   qrz", page1)
        font2 = QtGui.QFont()
        font2.setFamily("Arial")  # 括号里可以设置成自己想要的其它字体
        font2.setPointSize(12)
        self.label.setGeometry(1690, 105, 70, 50)  # 调整位置
        self.label.setFont(font2)

        self.labelName = QLabel(page1)
        font2 = QtGui.QFont()
        font2.setFamily("Arial")  # 括号里可以设置成自己想要的其它字体
        font2.setPointSize(12)
        self.labelName.setGeometry(1770, 105, 70, 50)  # 调整位置
        self.labelName.setFont(font2)

        # self.camera_list = ['电脑摄像头','测试视频']
        self.camera_list = GetFiles().getVideos()
        self.camera_list.append('电脑摄像头')
        self.camera_box = QComboBox(page1)
        self.camera_box.setGeometry(1585, 500, 200, 50)
        self.labelCamera = QLabel("视频流:", page1)
        self.labelCamera.setGeometry(1500, 500, 70, 50)  # 调整位置
        # 向下拉框添加选项
        for i in self.camera_list:
            self.camera_box.addItem(f'{i}')

        # .todo 按钮
        self.button1 = QPushButton("人脸签到打卡", page1)
        self.button1.setGeometry(1600, 700, 200, 100)
        self.button1.setCheckable(True)
        self.button1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        '''页面2'''
        page2 = QWidget()
        self.button_page2 = QPushButton("人脸信息录入")
        self.button_page2.setGeometry(130, 10, 150, 50)
        self.button_page2.setCheckable(True)
        self.button_page2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_page2.setParent(self)

        '''页面3'''
        page3 = QWidget()
        self.button_page3 = QPushButton("签到报表")
        self.button_page3.setGeometry(300, 10, 150, 50)
        self.button_page3.setCheckable(True)
        self.button_page3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_page3.setParent(self)

        self.button3_input = QPushButton("导入excel报表", page3)
        self.button3_input.setGeometry(100, 400, 200, 100)
        self.button3_input.setCheckable(True)
        self.button3_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button3_output = QPushButton("导出excel报表", page3)
        self.button3_output.setGeometry(100, 700, 200, 100)
        self.button3_output.setCheckable(True)
        self.button3_output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QVBoxLayout()
        self.widget = QWidget(page3)
        self.widget.setGeometry(450, 140, 1600, 900)
        self.widget.setStyleSheet("QWidget {background-color: #F5F5F5; \
                              border: 1px solid black;}")
        self.widget.setLayout(self.layout)
        self.table = QTableWidget(self)
        self.table.setGeometry(100, 100, 800, 600)
        self.layout.addWidget(self.table)

        self.stacked_widget.addWidget(page1)
        self.stacked_widget.addWidget(page2)
        self.stacked_widget.addWidget(page3)

    def slot_init(self):
        # 连接按钮的点击信号到切换页面的槽函数
        self.button_page1.clicked.connect(self.show_page1)
        self.button_page2.clicked.connect(self.show_page2)
        self.button_page3.clicked.connect(self.show_page3)
        self.button1.clicked.connect(self.run)
        self.button3_input.clicked.connect(self.input)
        self.button3_output.clicked.connect(self.output)

    def show_page1(self):
        if self.button_page1.isChecked():
            if self.button_list != []:
                for i in self.button_list:
                    if i != self.button_page1:
                        i.setChecked(False)
            self.button_list = []
            self.button_list.append(self.button_page1)
            self.stacked_widget.setCurrentIndex(0)

    def show_page2(self):
        if self.button_page2.isChecked():
            if self.button_list != []:
                for i in self.button_list:
                    if i != self.button_page2:
                        i.setChecked(False)
            self.button_list = []
            # self.button_list.append(self.button_page2)
            self.new_window = informationWindow()
            self.new_window.show()
            self.button_page2.setChecked(False)

    def show_page3(self):
        if self.button_page3.isChecked():
            if self.button_list != []:
                for i in self.button_list:
                    if i != self.button_page3:
                        i.setChecked(False)
            self.button_list = []
            self.button_list.append(self.button_page3)
            self.stacked_widget.setCurrentIndex(2)

    def input(self):
        if self.button3_input.isChecked():
            if self.button_list != []:
                for i in self.button_list:
                    if i != self.button3_input:
                        i.setChecked(False)
            self.button_list = []
            self.button_list.append(self.button3_input)
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(self, "加载Excel", "",
                                                       "Excel文件 (*.xlsx *.xls);;所有文件 (*)",
                                                       options=options)

            data = pd.read_excel(file_name, header=None)

            self.table.setRowCount(len(data))
            self.table.setColumnCount(len(data.columns))
            for i, row in enumerate(data.values):
                for j, value in enumerate(row):
                    print(i, j, value)
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(i, j, item)

            self.button3_input.setChecked(False)

    def output(self):
        if self.button3_output.isChecked():
            if self.button_list != []:
                for i in self.button_list:
                    if i != self.button3_output:
                        i.setChecked(False)
            self.button_list = []
            self.button_list.append(self.button3_output)
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "保存Excel", "",
                                                       "Excel文件 (*.xlsx);;所有文件 (*)",
                                                       options=options)
            if file_name:
                df = pd.DataFrame(columns=['Column {}'.format(i) for i in range(self.table.columnCount())])
                for i in range(self.table.rowCount()):
                    row_data = []
                    for j in range(self.table.columnCount()):
                        cell_item = self.table.item(i, j)
                        if cell_item is not None:
                            row_data.append(cell_item.text())
                        else:
                            row_data.append("")
                    print(row_data)
                    df.loc[i] = row_data
                print("df", df)
                df.to_excel(file_name, index=False, engine='openpyxl')
                print(f'数据已导出到 {file_name}')

            self.button3_output.setChecked(False)

    def run(self):
        if self.button1.isChecked():
            if self.button_list != []:
                for i in self.button_list:
                    if i != self.button1:
                        i.setChecked(False)
            self.button_list = []
            self.button_list.append(self.button1)
            print("self.table", self.table.columnCount())
            if self.table.columnCount() == 0 or self.table.rowCount() == 0:
                QMessageBox.warning(self, '提示', '请先导入签到列表')
            else:

                if self.camera_box.currentText() == "电脑摄像头":
                    camera_ip = 0
                else:
                    camera_ip = "video/" + self.camera_box.currentText()
                print("camera_ip", camera_ip)
                thread = MyThread(camera_ip, self.label_show1.height(), self.label_show1.width())
                thread.start()
                fr = face.FaceRecognition()
                while self.button1.isChecked():
                    frame, self.img_width, self.img_height = thread.get_frame()
                    print("frame")
                    pr_img_rbg, pr_img_rbg_face, name = fr.frun(frame)
                    #print("pr_img_rbg:", pr_img_rbg)
                    print("pr_img_rbg_face:", pr_img_rbg_face)
                    print("name:", name)
                    pr_img_rbg = cv2.cvtColor(pr_img_rbg, cv2.COLOR_BGR2RGB)
                    pr_img_rbg = QImage(pr_img_rbg.data, pr_img_rbg.shape[1], pr_img_rbg.shape[0],
                                        pr_img_rbg.shape[1] * 3, QImage.Format_RGB888)
                    self.label_show1.setPixmap(QPixmap(pr_img_rbg))
                    cv2.waitKey(5)
                    if pr_img_rbg_face is None or pr_img_rbg is None or name is None:
                        # if (pr_img_rbg==None) or (pr_img_rbg_face==None);
                        print("none")
                        continue
                    else:
                        for i in range(self.table.rowCount()):
                            # for j in range(self.table.columnCount()):
                            print("姓名", self.table.item(i, 0).text())
                            if name == self.table.item(i, 0).text():
                                print("已签到", name)
                                item = QTableWidgetItem("已签到")
                                self.table.setItem(i, 2, item)

                        pr_img_rbg_face = cv2.cvtColor(pr_img_rbg_face, cv2.COLOR_BGR2RGB)
                        pr_img_rbg_face = QImage(pr_img_rbg_face.data, pr_img_rbg_face.shape[1],
                                                 pr_img_rbg_face.shape[0], pr_img_rbg_face.shape[1] * 3,
                                                 QImage.Format_RGB888)
                        self.label_show2.setPixmap(QPixmap(pr_img_rbg_face))
                        self.labelname.setText(name)
                        cv2.waitKey(5)

                self.stop_thread(thread)

    def zh_ch(self, string):
        return string.encode("gbk").decode(errors="ignore")

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """

        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()