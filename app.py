from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms

# 设置上传文件夹路径 - 使用相对路径
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# 初始化 Flask 应用
app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为16MB

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 定义类别标签（KMNIST 数据集的 10 类）
CLASSES = ['お', 'き', 'す', 'つ', 'な', 'は', 'ま', 'や', 'れ', 'を']

# 定义模型结构
class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 初始化模型
model = ConvNet()

# 加载权重
MODEL_PATH = './model_batch_16.pth'
if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    print("Model loaded successfully")
else:
    print(f"Warning: Model file not found at {MODEL_PATH}")

# 设置为评估模式
model.eval()

# 图像预处理函数
def preprocess_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.resize((28, 28))
    img = transforms.ToTensor()(img)
    img = transforms.Normalize((0.5,), (0.5,))(img)
    img = img.unsqueeze(0)
    return img

# 检查文件类型是否合法
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # 1. 检查请求
        print("===== Upload Debug Info =====")
        print(f"Request method: {request.method}")
        print(f"Request files: {request.files}")
        print(f"Upload folder path: {UPLOAD_FOLDER}")
        print(f"Upload folder exists: {os.path.exists(UPLOAD_FOLDER)}")

        if 'file' not in request.files:
            print("Error: No file in request")
            return 'No file part', 400

        file = request.files['file']
        print(f"Received file: {file.filename}")

        if file.filename == '':
            print("Error: Empty filename")
            return 'No selected file', 400

        if file and allowed_file(file.filename):
            try:
                # 2. 保存文件
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(f"Attempting to save file to: {file_path}")

                # 确保上传目录存在
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                # 保存文件
                file.save(file_path)
                print(f"File saved successfully: {os.path.exists(file_path)}")

                # 3. 处理图像
                try:
                    image = preprocess_image(file_path)
                    print("Image preprocessed successfully")

                    # 4. 模型预测
                    with torch.no_grad():
                        output = model(image)
                        probabilities = torch.nn.functional.softmax(output, dim=1)
                        confidence, predicted_class = torch.max(probabilities, 1)

                    predicted_class = CLASSES[predicted_class.item()]
                    confidence = confidence.item() * 100  # 转换为浮点数并乘以100
                    print(f"Prediction complete: {predicted_class} ({confidence:.2f}%)")

                    # 5. 返回结果
                    image_url = url_for('serve_file', filename=filename)
                    print(f"Generated image URL: {image_url}")

                    return render_template(
                        'result.html',
                        image_path=image_url,
                        predicted_class=predicted_class,
                        confidence=f"{confidence:.2f}"  # 格式化为字符串
                    )

                except Exception as e:
                    print(f"Error in image processing: {str(e)}")
                    return f'Error processing image: {str(e)}', 500

            except Exception as e:
                print(f"Error saving file: {str(e)}")
                return f'Error saving file: {str(e)}', 500

        print("Invalid file type")
        return 'Invalid file type', 400

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return f'Unexpected error: {str(e)}', 500

@app.route('/uploads/<filename>')
def serve_file(filename):
    try:
        print(f"Attempting to serve file: {filename}")
        print(f"Full path: {os.path.join(UPLOAD_FOLDER, filename)}")
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return f'Error serving file: {str(e)}', 404

if __name__ == '__main__':
    print("\n=== Application Startup Checks ===")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Upload folder absolute path: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Upload folder exists: {os.path.exists(UPLOAD_FOLDER)}")
    
    # 测试目录权限
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        test_file = os.path.join(UPLOAD_FOLDER, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("Directory permissions test: SUCCESS")
    except Exception as e:
        print(f"Directory permissions test: FAILED - {str(e)}")
    
    app.run(debug=True)
