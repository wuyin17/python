import os
import time

import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QComboBox, QLineEdit, QMessageBox, QFileDialog
import glob

import time as tim

import xml.dom.minidom as xmldom


class informationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('New Window')
        self.face_detector = cv2.CascadeClassifier(
            'configuration/haarcascade_frontalface_default.xml')
        self.initUI()
        self.setGeometry(1000, 400, 350, 400)

    def initUI(self):
        # 创建一个标签

        self.choice_list = ['摄像头录入', '图片录入', '视频录入']
        self.choice_box = QComboBox(self)
        self.choice_box.setGeometry(150, 10, 150, 50)
        self.labelchoice = QLabel("录入方式：", self)
        self.labelchoice.setGeometry(50, 10, 100, 50)  # 调整位置
        # 向下拉框添加选项
        for i in self.choice_list:
            self.choice_box.addItem(f"{i}")

        self.label = QLabel('请输入姓名：', self)
        self.label.setGeometry(50, 125, 100, 50)
        self.text_input = QLineEdit(self)
        self.text_input.setGeometry(150, 125, 150, 50)

        self.button2 = QPushButton("开始录入", self)
        self.button2.setGeometry(125, 300, 100, 50)
        self.button2.clicked.connect(self.run)

    def run(self):
        print(self.text_input.text())
        if self.text_input.text() == '':
            QMessageBox.warning(self, '警告', '输入信息不能为空！')

        else:
            name = self.text_input.text()
            data_folder = "FaceData/" + name + "/"
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
            if self.choice_box.currentText() == "摄像头录入":
                cap = cv2.VideoCapture(0)
                start_time = time.time()
                count = 0
                while time.time() - start_time <= 3:
                    # print(start_time - time.time())
                    count += 1
                    ret, frame = cap.read()
                    if ret:
                        # self.img_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        # self.img_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        localtime = time.localtime(time.time())
                        bjtime = str(localtime[0]) + '年' + str(localtime[1]) + '月' + str(localtime[2]) + '日' + str(
                            localtime[3]) + '时' + str(localtime[4]) + '分' + str(localtime[5]) + '秒'
                        # if count%30==0:

                        # print("匹配成功：")
                        if count % 5 == 0:
                            cv2.imencode('.jpg', frame)[1].tofile(data_folder + name + "_" + bjtime + ".jpg")
                        # frame = cv2.resize(frame, (self.img_width, self.img_height))

                        # self.frame = frame
                        cv2.waitKey(1)
                    else:
                        cap.release()
                        cap = cv2.VideoCapture(0)
                cap.release()

            elif self.choice_box.currentText() == "视频录入":
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getOpenFileName(self, "加载视频", "",
                                                           "视频文件 (*.mp4 *.avi *.mov);;所有文件 (*)",
                                                           options=options)
                cap = cv2.VideoCapture(file_name)
                start_time = time.time()
                count = 0
                while (count) == 0:
                    # print(time.time()-start_time )
                    count += 1
                    print("count", count)
                    ret, frame = cap.read()
                    print(time.time() - start_time)

                    if ret:

                        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        face = self.face_detector.detectMultiScale(frame_gray)

                        if face == () or len(face) > 1:
                            continue
                        else:
                            # pr_img_rgb_face=[]
                            for x, y, w, h in face:
                                frame = frame[y:y + h, x:x + w]
                        if count == 30:
                            print("face", face)
                            print("frame", frame)
                        # self.img_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        # self.img_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        localtime = time.localtime(time.time())
                        bjtime = str(localtime[0]) + '年' + str(localtime[1]) + '月' + str(localtime[2]) + '日' + str(
                            localtime[3]) + '时' + str(localtime[4]) + '分' + str(localtime[5]) + '秒'
                        # if count%30==0:

                        # print("匹配成功！")

                        if count % 5 == 0:
                            print("count", count)
                            cv2.imencode('.jpg', frame)[1].tofile(data_folder + name + "_" + bjtime + ".jpg")
                            # cv2.waitKey(1)
                            print("count", count)
                        # frame = cv2.resize(frame, (self.img_width, self.img_height))
                        cv2.waitKey(1)
                        # self.frame = frame


                    if not ret:
                        print("break")
                        break

                cap.release()
            else:
                options = QFileDialog.Options()
                file_name, _ = QFileDialog.getOpenFileName(self, "加载图片", "",
                                                           "图片文件 (*.png *.jpg *.jpeg *.bmp);;所有文件 (*)",
                                                           options=options)

                img = cv2.imdecode(np.fromfile((os.path.join(file_name)), dtype=np.uint8), -1)
                # cv2.imshow("s:",img)
                localtime = time.localtime(time.time())
                bjtime = str(localtime[0]) + '年' + str(localtime[1]) + '月' + str(localtime[2]) + '日' + str(
                    localtime[3]) + '时' + str(localtime[4]) + '分' + str(localtime[5]) + '秒'
                cv2.imencode('.jpg', img)[1].tofile(data_folder + name + "_" + bjtime + ".jpg")
            QMessageBox.warning(self, '提示', '已经成功录入信息！')