import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QInputDialog, QLabel, QHBoxLayout
import json


#未使用

class DetectionApp(QWidget):
    def __init__(self, json_path):
        super().__init__()
        self.json_path = json_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Detection Results')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # 加载JSON文件
        with open(self.json_path, 'r') as f:
            self.results = json.load(f)

        for i, result in enumerate(self.results):
            result['id'] = i

        self.table = QTableWidget()
        self.table.setRowCount(len(self.results))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Label', 'Confidence', 'Corrected', 'Action'])

        for row, result in enumerate(self.results):
            self.table.setItem(row, 0, QTableWidgetItem(str(result['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(result['label']))
            self.table.setItem(row, 2, QTableWidgetItem("{:.2f}".format(result['confidence'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(result.get('corrected', False))))
            btn = QPushButton('Correct')
            btn.clicked.connect(lambda _, r=row: self.correct_detection(r))
            self.table.setCellWidget(row, 4, btn)

        layout.addWidget(self.table)

        # 添加关闭按钮，并触发其他方法
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.on_close_clicked)
        button_layout = QHBoxLayout()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def correct_detection(self, row):
        new_label, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter new label:')
        if ok:
            self.results[row]['label'] = new_label
            self.results[row]['corrected'] = True
            self.table.setItem(row, 1, QTableWidgetItem(new_label))
            self.table.setItem(row, 4, QTableWidgetItem('True'))
            self.save_results()

    def save_results(self):
        with open(self.json_path, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"Results saved to {self.json_path}")

    def on_close_clicked(self):
        # 在此处添加触发的其他方法逻辑
        print("Close button clicked, triggering another action.")

        self.close()


def main():
    json_path = '/demo/data/JSON/IMG_2113 4.json'  # 替换为你的JSON文件路径
    app = QApplication(sys.argv)
    ex = DetectionApp(json_path)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

