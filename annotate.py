import cv2
import numpy as np
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from shutil import copyfile
import pickle

third = int(640/3)


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 600

        oImage = QImage("Pepper.jpg")
        palette = QPalette()
        palette.setBrush(10, QBrush(oImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.crosshairs = np.ones((480, 640))*255
        third = int(640/3)

        cv2.line(self.crosshairs, (third, 0), (third, 480), (0, 0, 255), 1)
        cv2.line(self.crosshairs, (2*third, 0), (2*third, 480), (0, 0, 255), 1)

        cv2.imwrite("Output1.png", self.crosshairs)
        self.total_count = 0

        try:
            pickle_Rick = pickle.load(open("counter.pkl", "rb"))
            print("Current count: ", pickle_Rick[0])
            self.current_count = pickle_Rick[0]
        except EOFError:
            self.current_count = 1
        except IndexError:
            self.current_count = 1
        except FileNotFoundError:
            with open("counter.pkl", "wb") as f:
                pickle.dump([], f)
            self.current_count = 1

        self.filecount()
        self.file_name = "./SEG_final_rename/" + str(self.current_count) + ".png"
        self.out_file_dest = "./SEG_cleaned/"
        print("Total number of files: ", self.total_count)

        self.initUI()

    def filecount(self):
        for _ in os.listdir("./SEG_final_rename"):
            self.total_count += 1

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        btn = QPushButton("Close", self)
        btn.setToolTip("Close Application")
        btn.clicked.connect(self.closeEvent)
        btn.resize(btn.sizeHint())
        close = QHBoxLayout()
        close.addStretch(1)
        close.addWidget(btn)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(self.total_count)
        self.progress.setValue(self.current_count)
        self.progress_count = 0

        self.progress_label = QLabel(self)
        self.progress_label.setText("File:"  "(" + str(self.current_count) + "of" + str(self.total_count) + ")")

        progress_bar = QHBoxLayout()
        progress_bar.addSpacing(200)
        progress_bar.addWidget(self.progress)
        progress_bar.addWidget(self.progress_label)
        progress_bar.addSpacing(200)

        self.image_split()

        # Create widget
        self.label_left = QLabel(self)
        pixmap = QPixmap(QImage("left.png"))
        self.label_left.setPixmap(pixmap.scaled(100, 480))
        self.label_left.setScaledContents(True)
        self.label_left.resize(100, 480)

        self.label_center = QLabel(self)
        pixmap=QPixmap(QImage("center.png"))
        self.label_center.setPixmap(pixmap.scaled(100, 480))
        self.label_center.setScaledContents(True)
        self.label_center.resize(100, 480)

        self.label_right = QLabel(self)
        pixmap = QPixmap("right.png")
        self.label_right.setPixmap(pixmap.scaled(100, 400))
        self.label_right.setScaledContents(True)
        self.label_right.resize(100, 480)

        images_box = QHBoxLayout()
        images_box.addWidget(self.label_left)
        images_box.addSpacing(5)
        images_box.addWidget(self.label_center)
        images_box.addSpacing(5)
        images_box.addWidget(self.label_right)

        self.forward = QShortcut(QKeySequence("w"), self)
        self.forward.activated.connect(self.on_click_straight)

        self.left = QShortcut(QKeySequence("a"), self)
        self.left.activated.connect(self.on_click_left)

        self.right = QShortcut(QKeySequence("d"), self)
        self.right.activated.connect(self.on_click_right)

        self.skip = QShortcut(QKeySequence("s"), self)
        self.skip.activated.connect(self.on_click_skip)


        straight_button = QPushButton("Straight (w)", self)
        straight_button.setToolTip("Press 'w' to move image to Straight category")
        straight_button.move(280, 550)
        straight_button.clicked.connect(self.on_click_straight)

        left_button = QPushButton("Left (a)", self)
        left_button.setToolTip("Press 'a' to move image to Left category")
        left_button.move(280, 550)
        left_button.clicked.connect(self.on_click_left)

        right_button = QPushButton("Right (d)", self)
        right_button.setToolTip("Press 'd' to move image to Right category")
        right_button.move(280, 550)
        right_button.clicked.connect(self.on_click_right)

        skip_button = QPushButton("Skip (s)", self)
        skip_button.setToolTip("Press 's'. This will not move the current image to annotation directory")
        skip_button.move(280, 600)
        skip_button.clicked.connect(self.on_click_skip)

        buttons_box = QHBoxLayout()
        buttons_box.addSpacing(200)
        buttons_box.addWidget(left_button)
        buttons_box.addWidget(straight_button)
        buttons_box.addWidget(right_button)
        buttons_box.addSpacing(200)

        buttons_box_bottom = QHBoxLayout()
        buttons_box_bottom.addSpacing(300)
        buttons_box_bottom.addWidget(skip_button)
        buttons_box_bottom.addSpacing(300)

        buttons_box_main = QVBoxLayout()
        buttons_box_main.addStretch(1)
        buttons_box_main.addLayout(buttons_box)
        buttons_box_main.addLayout(buttons_box_bottom)

        main_frame = QVBoxLayout()
        main_frame.addStretch(1)
        main_frame.addLayout(images_box)
        main_frame.addLayout(progress_bar)
        main_frame.addLayout(buttons_box_main)
        main_frame.addLayout(close)

        self.setLayout(main_frame)

        self.show()

    def on_click_straight(self):
        print('PyQt5 button click _ straight')
        self.progress_count += 1
        self.current_count += 1
        self.progress_label.setText("File:"  "(" + str(self.current_count) + "of" + str(self.total_count) + ")")
        self.progress.setValue(self.progress_count)
        outfile = "./SEG_cleaned/Straight/" + str(self.current_count-1) + ".png"
        copyfile(self.file_name,outfile)
        self.file_name = "./SEG_final_rename/" + str(self.current_count) + ".png"
        self.image_split()
        pixmap = QPixmap("center.png")
        self.label_center.setPixmap(pixmap.scaled(100, 400))
        pixmap = QPixmap("left.png")
        self.label_left.setPixmap(pixmap.scaled(100, 400))
        pixmap = QPixmap("right.png")
        self.label_right.setPixmap(pixmap.scaled(100, 400))

    def on_click_left(self):
        print('PyQt5 button click _ left')
        self.progress_count += 1
        self.current_count += 1
        self.progress_label.setText("File:"  "(" + str(self.current_count) + "of" + str(self.total_count) + ")")
        self.progress.setValue(self.progress_count)
        outfile = "./SEG_cleaned/Left/" + str(self.current_count - 1) + ".png"
        copyfile(self.file_name, outfile)
        self.file_name = "./SEG_final_rename/" + str(self.current_count) + ".png"
        self.image_split()
        pixmap = QPixmap("center.png")
        self.label_center.setPixmap(pixmap.scaled(100, 400))
        pixmap = QPixmap("left.png")
        self.label_left.setPixmap(pixmap.scaled(100, 400))
        pixmap = QPixmap("right.png")
        self.label_right.setPixmap(pixmap.scaled(100, 400))

    def on_click_right(self):
        print('PyQt5 button click _ right')
        self.progress_count += 1
        self.current_count += 1
        self.progress_label.setText("File:"  "(" + str(self.current_count) + "of" + str(self.total_count) + ")")
        self.progress.setValue(self.progress_count)
        outfile = "./SEG_cleaned/Right/" + str(self.current_count - 1) + ".png"
        copyfile(self.file_name, outfile)
        self.file_name = "./SEG_final_rename/" + str(self.current_count) + ".png"
        self.image_split()
        pixmap = QPixmap("center.png")
        self.label_center.setPixmap(pixmap.scaled(100, 400))
        pixmap = QPixmap("left.png")
        self.label_left.setPixmap(pixmap.scaled(100, 400))
        pixmap = QPixmap("right.png")
        self.label_right.setPixmap(pixmap.scaled(100, 400))

    def on_click_skip(self):
        print('PyQt5 button click _ skip')
        self.progress_count += 1
        self.current_count += 1
        self.progress_label.setText("File:"  "(" + str(self.current_count) + "of" + str(self.total_count) + ")")
        self.progress.setValue(self.progress_count)
        self.file_name = "./SEG_final_rename/" + str(self.current_count) + ".png"
        self.image_split()
        pixmap = QPixmap("center.png")
        self.label_center.setPixmap(pixmap.scaled(100, 400))
        pixmap = QPixmap("left.png")
        self.label_left.setPixmap(pixmap.scaled(100, 400))
        pixmap = QPixmap("right.png")
        self.label_right.setPixmap(pixmap.scaled(100, 400))

    def image_split(self):
        img = cv2.imread(self.file_name)
        imgL = img[:, 0:third, :]
        imgC = img[:, third:2 * third, :]
        imgR = img[:, 2 * third:, :]

        imgL = imgL.copy()
        imgC = imgC.copy()
        imgR = imgR.copy()

        cv2.imwrite("left.png", imgL)
        cv2.imwrite("center.png", imgC)
        cv2.imwrite("right.png", imgR)

    def closeEvent(self, event):

        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
            QMessageBox.Save)

        if reply == QMessageBox.Close:
            with open('counter.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([self.current_count], f)
            app.quit()
        elif reply == QMessageBox.Save:
            with open('counter.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([self.current_count], f)
        else:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())