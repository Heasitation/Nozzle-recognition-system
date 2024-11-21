import os
import json
import cv2


# 定义保存标注图片的路径
annotated_image_dir = 'data/annotated_images'
os.makedirs(annotated_image_dir, exist_ok=True)

# 定义颜色字典，根据不同的标签使用不同颜色
label_colors = {
    'not have': (0, 255, 0),  # 绿色
    'have': (0, 0, 255),  # 红色
    # 添加更多标签及其对应的颜色
}

# 定义一个函数来从 JSON 文件中读取预测结果并绘制标签和边界框
def draw_labels_on_image(json_path):
    # 读取 JSON 文件
    with open(json_path, 'r') as f:
        predictions = json.load(f)

    # 获取图像路径
    image_path = predictions[0]['image']
    image = cv2.imread(image_path)
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    # 按置信度对预测结果进行排序，置信度高的先绘制
    predictions_sorted = sorted(predictions, key=lambda x: x['confidence'], reverse=True)

    # 已绘制框的集合，用于检查重叠
    drawn_boxes = []

    # 遍历每个预测框并绘制标签
    for prediction in predictions_sorted:
        label = prediction['label']
        confidence = prediction['confidence']
        bbox = prediction['bbox']
        pred_id = prediction['id']  # 获取ID
        x, y, w, h = map(int, bbox)

        # 计算边界框的左上角和右下角坐标
        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)

        # 根据标签获取颜色
        color = label_colors.get(label, (255, 0, 0))  # 默认为蓝色

        # 检查当前框是否与已绘制的框重叠
        skip_box = False
        for drawn_box in drawn_boxes:
            if x1 < drawn_box[2] and x2 > drawn_box[0] and y1 < drawn_box[3] and y2 > drawn_box[1]:
                skip_box = True
                break

        if skip_box:
            continue  # 如果重叠，则跳过绘制当前框

        # 在图像上绘制边界框
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

        
        # 构造标签文本，ID放在标签前面，并且在同一行显示
        label_text = f'{pred_id}: {label} ({confidence:.2f})'

        # 根据边界框的长宽中较大的一边动态调整字体大小
        font_scale = max(w, h) / 170
        font_thickness = max(1, int(font_scale * 1.5))
        outline_thickness = font_thickness + 1

        # 获取文本大小
        text_size, _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, outline_thickness)

        # 在边界框上方绘制标签和唯一的 ID
        text_x = x1
        text_y = y1 - 10 if y1 - 10 > 10 else y2 + text_size[1] + 10

        # 绘制文本背景
        cv2.rectangle(image, (text_x - 2, text_y - text_size[1] - 2), (text_x + text_size[0] + 2, text_y + 2), (255, 0, 0), -1)
        # 绘制描边
        cv2.putText(image, label_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), outline_thickness, cv2.LINE_AA)
        # 绘制文本
        cv2.putText(image, label_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

        # 添加当前框到已绘制框的集合
        drawn_boxes.append((x1, y1, x2, y2))

    # 保存标注后的图像，不进行大小调整
    annotated_image_path = os.path.join(annotated_image_dir, f'{image_name}_annotated.jpg')
    cv2.imwrite(annotated_image_path, image)
    print(f"Annotated image saved to {annotated_image_path}")



    return annotated_image_path

