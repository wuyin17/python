import multiprocessing
import sys
from PyQt5.QtWidgets import QApplication 
from FaceRecognition.ui.mainWindow import Ui_MainWindow


if __name__ == '__main__':
    multiprocessing.freeze_support()
    App = QApplication(sys.argv)
    # config = r"F:/Aircraft inspection/plane/TriwebAiPlane/config.json"
    win = Ui_MainWindow()
    win.setStyleSheet("""
        QWidget {
            background-color: rgb(255, 206, 250); /* 白色背景 */
        }
    """)
    win.show()
    sys.exit(App.exec())
