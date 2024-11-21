import json
import os
from PyQt5 import QtGui
from ultralytics import YOLO

#根据模型和原图输出结果/图片检测并输出json文件

def opop(model,img,img_path):
    # 引入模型
    model = YOLO(model)
    # 通过引用模型进行图像检测
    results = model.predict(source=img, conf=0.75, iou=0.5)
    # results = model.predict(source=img)
    annotated_frame = results[0].plot()
    predictions = []
    # for result in results:
    #     for box in result.boxes:
    #         prediction = {
    #             'image': result.path,  # 图片路径
    #             'label': model.names[int(box.cls)],  # 类别标签
    #             'confidence': float(box.conf),  # 置信度
    #             'bbox': [float(coord) for coord in box.xywh[0].tolist()]  # 边界框 [x, y, w, h]
    #         }
    #         predictions.append(prediction)


    # 指定保存路径
    save_dir = 'data/JSON'  # 替换为你想要保存文件的目录路径
    os.makedirs(save_dir, exist_ok=True)  # 如果目录不存在，则创建

    # 逐张图片保存预测结果为 JSON 文件
    for result in results:
        predictions = []
        image_path = img_path

        # 添加ID计数器
        id_counter = 0

        for box in result.boxes:
            prediction = {
                'id': id_counter,  # 添加唯一ID
                'image': image_path,  # 图片路径
                'label': model.names[int(box.cls)],  # 类别标签
                'confidence': float(box.conf),  # 置信度
                'bbox': [float(coord) for coord in box.xywh[0].tolist()]  # 边界框 [x, y, w, h]
            }
            predictions.append(prediction)
            id_counter += 1  # 增加ID计数器



    # 保存预测结果为 JSON 文件
    save_path = os.path.join(save_dir, 'predictions.json')
    with open(save_path, 'w') as f:
        json.dump(predictions, f, indent=4)

    print(f"Predictions saved to {save_path}")


    # 将图像数据转换为QImage格式
    height, width, channel = annotated_frame.shape
    bytes_per_line = 3 * width
    qimage = QtGui.QImage(annotated_frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
    # 将QImage转换为QPixmap
    pixmap = QtGui.QPixmap.fromImage(qimage)

    return pixmap