from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

# 初始化 Flask 应用
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # 上传文件的存储路径
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}  # 允许的文件类型

# 定义类别标签（KMNIST 数据集的 10 类）
CLASSES = ['お', 'き', 'す', 'つ', 'な', 'は', 'ま', 'や', 'れ', 'を']

# 检查文件类型是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# 图像预处理函数
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')  # 转为灰度图
    img = img.resize((28, 28))  # KMNIST 数据集的输入尺寸为 28x28
    img_array = np.array(img) / 255.0  # 归一化
    img_array = np.expand_dims(img_array, axis=0)  # 添加批次维度
    img_array = np.expand_dims(img_array, axis=-1)  # 添加通道维度
    return img_array

# ---------------------- 伪模型阶段 ----------------------
# 模拟一个伪模型
def fake_predict(img_array):
    import random
    predicted_class = random.choice(CLASSES)  # 随机选择一个类别
    confidence = random.uniform(80, 100)  # 随机生成置信度（80% 到 100%）
    return predicted_class, confidence
# ---------------------- 伪模型阶段结束 ----------------------

# ---------------------- 真实模型阶段 ----------------------
# 当模型文件准备好后，替换伪模型为真实模型
# from tensorflow.keras.models import load_model
# model = load_model('model/kmnist_model.h5')  # 加载训练好的模型
# def real_predict(img_array):
#     predictions = model.predict(img_array)
#     predicted_class = CLASSES[np.argmax(predictions)]
#     confidence = np.max(predictions) * 100
#     return predicted_class, confidence
# ---------------------- 真实模型阶段结束 ----------------------

# 路由：主页（上传页面）
@app.route('/')
def index():
    return render_template('index.html')

# 路由：处理上传的文件
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))  # 如果没有文件，重定向到主页

    file = request.files['file']
    if file and allowed_file(file.filename):
        # 保存上传的文件
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # 预处理图像
        img_array = preprocess_image(file_path)

        # ---------------------- 替换点 ----------------------
        # 使用伪模型进行预测
        predicted_class, confidence = fake_predict(img_array)

        # 如果模型文件已准备好，替换为真实模型预测
        # predicted_class, confidence = real_predict(img_array)
        # ---------------------- 替换点结束 ----------------------

        # 渲染结果页面
        return render_template('result.html', 
                               image_path=file_path, 
                               predicted_class=predicted_class, 
                               confidence=confidence)
    else:
        return redirect(url_for('index'))

# 启动应用
if __name__ == '__main__':
    # 确保上传目录存在
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
