import cv2
from PyQt5 import QtCore

from ultralytics import YOLO
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt


#用已有模型对视频中的工件预测并输出视频

class VideoWindow(QWidget):
    def __init__(self, video_path,model):
        super().__init__()
        self.setWindowTitle("视频检测")
        self.video_path = video_path
        self.model = YOLO(model)
        self.cap = cv2.VideoCapture(video_path)

        # 创建标签用于显示视频
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setEnabled(True)
        self.label.setMaximumSize(QtCore.QSize(1500, 800))
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 使用QTimer定时更新视频帧
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(int(1000 / self.cap.get(cv2.CAP_PROP_FPS)))

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.timer.stop()
            self.cap.release()
            return

        # 使用YOLOv8模型对当前帧进行推理
        results = self.model(frame)

        # 绘制检测结果
        for result in results:
            for box in result.boxes:
                confidence = box.conf[0]

                # 仅显示置信度高于0.8的检测结果
                if confidence >= 0.8:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    label = box.cls

                    # 将检测结果中的标签转换为自定义标签
                    custom_label = 'have' if label == 0 else 'not have'

                    # 根据自定义标签设置边框颜色
                    color = (0, 255, 0) if custom_label == 'have' else (0, 0, 255)

                    # 绘制边界框和标签
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, f'{custom_label}: {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                color, 2)

        # 将处理后的帧转换为QImage并显示在标签中
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame_rgb.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_img))

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        event.accept()


