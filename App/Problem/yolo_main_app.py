
from ultralytics import YOLO
import time
import math
import sys
import cv2
import serial
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QTextEdit, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QSize, QDateTime, QPropertyAnimation, QEasingCurve, QTimer,QCoreApplication
ser = serial.Serial('COM6', 9600)
video_path = 'E:/Research_Papers/Autonomous Pollination/Resource/Video_image/video_480x640.mp4'

# Initialize FPS calculation variables

printed_ids = set()
prev_frame_time = 0
fps_sum = 0
frame_count = 0

button_height=35
class HoverButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(
            "color: black; background-color: white; border: 2px solid #BC006C; border-radius: 10px; height: 50%; font-size: 24px;"
        )

    def enterEvent(self, event):
        self.hover_animation = QPropertyAnimation(self, b"background-color")
        self.hover_animation.setStartValue(Qt.white)
        self.hover_animation.setEndValue(Qt.magenta)
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.hover_animation.start()

    def leaveEvent(self, event):
        self.hover_animation = QPropertyAnimation(self, b"background-color")
        self.hover_animation.setStartValue(Qt.magenta)
        self.hover_animation.setEndValue(Qt.white)
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.hover_animation.start()

class ImageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.model_det = None
        # Set up the main layout
        main_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignLeft)

        # Left widget with a fixed width
        left_widget = QWidget()
        left_widget.setFixedWidth(400)  # Fixed width
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignTop)
        left_layout.setContentsMargins(10, 10, 10, 10)

        # Set the background color using palette
        palette = left_widget.palette()
        palette.setColor(left_widget.backgroundRole(), Qt.darkGray)
        left_widget.setPalette(palette)

        # App name label with doubled text size
        app_name_label = QLabel("Tomato Flower Detection")
        app_name_label.setStyleSheet("color: white; font-size: 34px;")  # Double text size
        left_layout.addWidget(app_name_label)

        # # Dropdown menu with six options
        # options = ["YOLOv8_Nano", "YOLOv8_Small", "YOLO-NAS", "YOLOv7", "YOLOv5_Nano", "YOLOv5_Small"]
        # self.dropdown_menu = QComboBox(self)
        # self.dropdown_menu.addItems(options)
        # self.dropdown_menu.setObjectName('dropdown_menu')  # Set object name for finding child later
        # font = QFont()
        # font.setPointSize(14)  # Set the font size to 14 points
        # self.dropdown_menu.setFont(font)
        # self.dropdown_menu.setStyleSheet("color: white; background-color: #0d0207; border: 3px solid #BC006C; border-radius: 15px; height: 33%;")
        # left_layout.addWidget(self.dropdown_menu)

        # Button to load image (with functionality) with doubled text size
        load_button_1 = HoverButton("Saved Image Detection")
        load_button_1.clicked.connect(self.choose_image)
        load_button_1.setMinimumHeight(button_height)  # Set a fixed minimum height
        left_layout.addWidget(load_button_1)
        
        load_button_5 = HoverButton(f"Real-Time Image Detection")
        load_button_5.clicked.connect(self.update_webcam_image)
        load_button_5.setMinimumHeight(button_height)  # Set a fixed minimum height
        left_layout.addWidget(load_button_5)
        
        load_button_4 = HoverButton(f"Real-Time Localization")
        load_button_4.clicked.connect(lambda: self.capture_from_webcam())
        load_button_4.setMinimumHeight(button_height)  # Set a fixed minimum height
        left_layout.addWidget(load_button_4)
        
    
        load_button_3 = HoverButton(f"Heat Map Visulaization")
        load_button_3.clicked.connect(lambda: self.d())
        load_button_3.setMinimumHeight(button_height)  # Set a fixed minimum height
        left_layout.addWidget(load_button_3)
        
        # # Button to capture image from webcam
        # load_button_2 = HoverButton("Localization via Segmentation")
        # load_button_2.clicked.connect(lambda: self.update_webcam_image(2))
        # load_button_2.setMinimumHeight(button_height)  # Set a fixed minimum height
        # left_layout.addWidget(load_button_2)

        # Additional buttons without functionality with doubled text size

        # Text box (read-only) with doubled text size
        text_box = QTextEdit()
        text_box.setReadOnly(True)  # Set the QTextEdit as read-only
        text_box.setObjectName('text_box')  # Set object name for finding child later
        text_box.setStyleSheet("color: black; background-color: white; border: 2px solid #BC006C; border-radius: 10px; font-size: 24px;")  # Double text size
        left_layout.addWidget(text_box)

        # Add left widget to the main layout
        main_layout.addWidget(left_widget)
        # Right widget for image display
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignCenter)  # Align center both horizontally and vertically
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_widget.setStyleSheet("border: 3px solid #ffffff; background-color: #ffffff;")  # Set border color
        

        self.image_label = QLabel()
        right_layout.addWidget(self.image_label)  # Add the image_label to the right layout

        # Add right widget to the main layout
        main_layout.addWidget(right_widget)

        # Set up the main window
        self.setLayout(main_layout)
        self.setFixedSize(950, 700)  # Adjusted window size
        self.setWindowTitle("Tomato FLower Detection")
        self.setStyleSheet("background-color: #000000;")

        # Variables for webcam capture
        self.webcam = cv2.VideoCapture(video_path)  # Use the default webcam (you may need to adjust the index)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_webcam_video)

    def choose_image(self):
        selected_model_name = self.dropdown_menu.currentText()
        # model_path = f'E:/Research_Papers/weed_detect/Code/All code/Models/{selected_model_name}.onnx'
        model_path = f'E:/Research_Papers/Autonomous Pollination/model/best.pt'
        # model_path_seg = f'E:/Research_Papers/weed_detect/Code/All code/Models/{selected_model_name}_seg.onnx'
        model_det=YOLO(model_path)
        # model_seg=YOLO(model_path_seg)
        
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        file_dialog.setViewMode(QFileDialog.Detail)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                image_path = selected_files[0]
                img=cv2.imread(image_path)
                results = model_det.track(img, stream=False, imgsz=(256,640))
                annotated_frame = results[0].plot()
                
                rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(convert_to_Qt_format)
                pixmap = pixmap.scaled(QSize(800, 800), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                # Set the resized pixmap to the label
                self.image_label.setPixmap(pixmap)


    def update_webcam_image(self):
        selected_model_name = self.dropdown_menu.currentText()
        # model_path = f'E:/Research_Papers/weed_detect/Code/All code/Models/{selected_model_name}.onnx'
        model_path = f'E:/Research_Papers/Autonomous Pollination/model/best.pt'
        # model_path_seg = f'E:/Research_Papers/weed_detect/Code/All code/Models/{selected_model_name}_seg.onnx'
        model_det=YOLO(model_path)
        # model_seg=YOLO(model_path_seg)
        self.timer.start(1)
        ret, frame = self.webcam.read()
        if ret:
            results = model_det.track(frame, stream=False, imgsz=(256,640))
            annotated_frame = results[0].plot()
            
            rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
            pixmap = pixmap.scaled(QSize(800, 800), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # Set the resized pixmap to the label
            self.image_label.setPixmap(pixmap)
        self.timer.stop()
    
    def capture_from_webcam(self):
        if self.timer.isActive():
            self.timer.stop()
            print("cccc")
            
        else:
            # selected_model_name = self.dropdown_menu.currentText()
            model_path = f'E:/Research_Papers/Autonomous Pollination/model/best.pt'
            self.model_det = YOLO(model_path)  # Update this line
            self.timer.start(1)

    def update_webcam_video(self):
        global prev_frame_time, fps_sum, frame_count
        ret, frame = self.webcam.read()
        if ret:
            cropped_frame = frame[:, :]
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = self.model_det.track(cropped_frame, persist=True, conf=0.7, iou=0.5, imgsz=(640, 480), verbose=False, classes=1)
            output_tensor = results[0].boxes.id     # boxes is paramter while id is attribute.
            if output_tensor is not None:
                output_integers_id = [int(x) for x in output_tensor]
                output_tensor_box = results[0].boxes.xyxy
                output_integers_box = [[int(round(float(value))) for value in tensor] for tensor in output_tensor_box]
                # print(output_integers_id)
                unchecked_num = [num for num in output_integers_id if num not in printed_ids]
                if unchecked_num:
                    choosen_value = min(unchecked_num)
                    bbox = None  # Initialize bbox variable outside the loop
                    counter=0
                    while counter < 10:         
                        ret, frame = self.webcam.read()
                        cropped_frame = frame[:, :]
                        # Run YOLOv8 tracking on the frame, persisting tracks between frames
                        results = self.model_det.track(cropped_frame, persist=True, conf=0.7, iou=0.5, imgsz=(640, 480), verbose=False, classes=1)
                        annotated_frame = results[0].plot()
                        rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                        h, w, ch = rgb_image.shape
                        bytes_per_line = ch * w
                        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                        pixmap = QPixmap.fromImage(convert_to_Qt_format)
                        self.image_label.setPixmap(pixmap)
                        QCoreApplication.processEvents()
                        # text_edit = self.findChild(QTextEdit)
                        # text_edit.clear()
                        # text_edit.append(f'Mature Flower Count: {len(printed_ids)}')
                        output_tensor = results[0].boxes.id
                        if output_tensor is not None:
                            output_integers_id = [int(x) for x in output_tensor]
                            output_tensor_box = results[0].boxes.xyxy
                            output_integers_box = [[int(round(float(value))) for value in tensor] for tensor in output_tensor_box]
                            try:
                                # Find the index of the object with the specified ID
                                index = output_integers_id.index(choosen_value)
                                # Get the corresponding bounding box value
                                bbox = output_integers_box[index]
                                # Print the bounding box for debugging
                                centerX = (bbox[0] + bbox[2]) // 2
                                centerY = (bbox[1] + bbox[3]) // 2
                                print(centerX, centerY)
                                ser.write(f"{centerX},{centerY}\n".encode())
                                time.sleep(1)
                                # print("Bounding box for object with ID",counter,"--", choosen_value, ":", bbox)                        
                            except ValueError:
                                pass
                            
                        counter += 1
                        
                    printed_ids.add(choosen_value)
            annotated_frame = results[0].plot()# print(printed_ids)
            rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
    
            # Reduce the width while maintaining the aspect ratio
            desired_width = 400  # Set this to your desired width
            resized_pixmap = pixmap.scaledToWidth(desired_width, Qt.SmoothTransformation)
            # Set the resized pixmap to the label
            self.image_label.setPixmap(pixmap)
            text_edit = self.findChild(QTextEdit)
            text_edit.clear()
            text_edit.append(f'Mature Flower Count: {len(printed_ids)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageApp()
    window.show()
    sys.exit(app.exec_())
