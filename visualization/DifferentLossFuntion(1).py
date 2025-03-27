import pandas as pd
import matplotlib.pyplot as plt

def read_and_process_csv(file_path):
    """
    读取CSV文件并处理数据

    参数:
    file_path: CSV文件的路径

    返回:
    loss_function_data_dict: 字典，键为损失函数名称，值为包含训练数据的DataFrame
    """
    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 将 'Epoch' 列转换为字符串类型
    df['Epoch'] = df['Epoch'].astype(str)

    # 处理 'train_accuracy' 和 'test_accuracy' 列：去掉百分号并转换为浮点数
    df['train_accuracy'] = df['train_accuracy'].str.rstrip('%').astype(float)
    df['test_accuracy'] = df['test_accuracy'].str.rstrip('%').astype(float)

    # 处理异常值（例如 train_loss 列中的 396）
    df = df[df['train_loss'] < 100]  # 过滤掉 train_loss 大于 100 的异常值

    # 初始化字典
    loss_function_data_dict = {}

    # 获取所有唯一的损失函数名称
    loss_functions = df['Loss Function'].unique()

    # 遍历每个损失函数
    for loss_function in loss_functions:
        # 筛选出当前损失函数的数据
        data = df[df['Loss Function'] == loss_function]

        # 将数据存储到字典中
        loss_function_data_dict[loss_function] = data

    return loss_function_data_dict

def plot_loss_function_comparison(loss_function_data_dict, save_path=None, figsize=(12, 8)):
    """
    绘制不同损失函数的性能比较图

    参数:
    loss_function_data_dict: 字典，键为损失函数名称，值为包含训练数据的DataFrame
                            每个DataFrame应包含列：'Epoch', 'train_loss', 'train_accuracy', 'test_accuracy'
    save_path: 字符串，图表保存路径，默认为None（不保存）
    figsize: 元组，图表尺寸

    返回:
    matplotlib图表对象
    """
    plt.figure(figsize=figsize)

    # 绘制训练损失
    plt.subplot(2, 2, 1)
    for loss_function, data in loss_function_data_dict.items():
        plt.plot(data['Epoch'], data['train_loss'], label=loss_function)
    plt.xlabel('Epoch')
    plt.ylabel('Training Loss')
    plt.title('Training Loss Comparison')
    plt.legend()

    # 绘制训练准确率
    plt.subplot(2, 2, 2)
    for loss_function, data in loss_function_data_dict.items():
        plt.plot(data['Epoch'], data['train_accuracy'], label=loss_function)
    plt.xlabel('Epoch')
    plt.ylabel('Training Accuracy')
    plt.title('Training Accuracy Comparison')
    plt.legend()

    # 绘制测试准确率
    plt.subplot(2, 2, 3)
    for loss_function, data in loss_function_data_dict.items():
        plt.plot(data['Epoch'], data['test_accuracy'], label=loss_function)
    plt.xlabel('Epoch')
    plt.ylabel('Test Accuracy')
    plt.title('Test Accuracy Comparison')
    plt.legend()

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)

    plt.show()

# CSV文件路径
file_path = r"C:\Users\Richard song\Documents\WeChat Files\wxid_qmk43aaf1rcv11\FileStorage\File\2025-03\1_DifferentLossFuntion.csv"  # 替换为你的CSV文件路径

# 读取并处理CSV文件
loss_function_data_dict = read_and_process_csv(file_path)

# 调用函数绘制图表
plot_loss_function_comparison(loss_function_data_dict)