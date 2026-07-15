import cv2
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
import glob
import time as tim
import xml.dom.minidom as xmldom

class FaceRecognition:
    def __init__(self, folder_path="FaceData"):
        self.face_detector = cv2.CascadeClassifier(
            'configuration/haarcascade_frontalface_default.xml')
        self.images_gray, self.images_rbg, self.labels, self.names = self.load_dataset(folder_path)
        count = 0
        for i, j in zip(self.images_gray, self.images_rbg):
            face = self.face_detector.detectMultiScale(i)
            for x, y, w, h in face:
                self.images_gray[count] = i[y:y + h, x:x + w]
                # cv2.imshow("s", images[count])
                # cv2.waitKey(0)
                self.images_rbg[count] = j[y:y + h, x:x + w]
            count += 1
        # 创建LBPHFaceRecognizer实例并训练
        self.recognizer = cv2.face.LBPHFaceRecognizer.create()
        self.recognizer.train(self.images_gray, np.array(self.labels))
        print("人脸识别系统运行中...")

    def load_dataset(self, folder_path):
        names = []
        images_gray = []
        images_rbg = []
        labels = []
        ID = 0
        for name in os.listdir(folder_path):
            subpath = os.path.join(folder_path, name)
            if os.path.isdir(subpath):
                names.append(name)
                for file in os.listdir(subpath):
                    images_rbg.append(cv2.imdecode(np.fromfile((os.path.join(subpath, file)), dtype=np.uint8), -1))
                    images_gray.append(
                        cv2.imdecode(np.fromfile((os.path.join(subpath, file)), dtype=np.uint8), cv2.IMREAD_GRAYSCALE))
                    labels.append(ID)
                ID += 1

        return images_gray, images_rbg, labels, names



    def frun(self, pr_img_rbg):
        pr_img_gray = cv2.cvtColor(pr_img_rbg, cv2.COLOR_BGR2GRAY)
        face = self.face_detector.detectMultiScale(pr_img_gray)
        # 在图片中对人脸画矩形
        print("facedetected", face)
        if face == ():
            return pr_img_rbg, None, None
        else:
            # pr_img_rbg_face=[]:
            for x, y, w, h in face:
                pr_img_gray = pr_img_gray[y:y + h, x:x + w]
                pr_img_rbg_face = pr_img_rbg[y:y + h, x:x + w]

            # 进行预测
            if pr_img_gray is None or pr_img_gray.shape[0] < 1 or pr_img_gray.shape[1] < 1:
                print("Image has invalid size")
                return pr_img_rbg, None, None
            else:
                # print("gray frame shape: {}".format(gray_frame.shape))
                label, confidence = self.recognizer.predict(pr_img_gray)
                if confidence > 70:
                    return pr_img_rbg, None, None
                name = self.names[label]
                cv2.rectangle(pr_img_rbg, (int(x), int(y)), (int(x + w), int(y + h)),
                              (0, 255, 0), 2)

                pilimg = Image.fromarray(pr_img_rbg)
                # PIL图片上打印汉字
                draw = ImageDraw.Draw(pilimg)  # 图片上打印

                font = ImageFont.truetype(font="./font/SourceHanSansSC-Normal.ttf", size=20,
                                          encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
                print("ok")
                draw.text(xy=(int(x), int(y) - 30),
                          text="姓名" + "+" + name,
                          fill=(0, 255, 0), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
                print("ok")
                pr_img_rbg = np.array(pilimg)
                print("ok")

                # pr_img_rbg = cv2.putText(pr_img_rbg,
                #             "姓名:"+name,
                #             (int(x), int(y) - 5),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                #
                count_label = 0
                for i in range(label + 1):
                    count_label += self.labels.count(i)
                return pr_img_rbg, pr_img_rbg_face, name