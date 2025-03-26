import pandas as pd
import matplotlib.pyplot as plt

def read_and_process_csv(file_path):
    """
    读取CSV文件并处理数据

    参数:
    file_path: CSV文件的路径

    返回:
    batch_size_data_dict: 字典，键为批量大小，值为包含训练数据的DataFrame
    """
    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 将 'epoch' 列转换为字符串类型
    df['epoch'] = df['epoch'].astype(str)

    # 处理 'train_accuracy' 和 'test_accuracy' 列：去掉百分号并转换为浮点数
    df['train_accuracy'] = df['train_accuracy'].str.rstrip('%').astype(float)
    df['test_accuracy'] = df['test_accuracy'].str.rstrip('%').astype(float)

    # 初始化字典
    batch_size_data_dict = {}

    # 获取所有唯一的批量大小
    batch_sizes = df['batch_size'].unique()

    # 遍历每个批量大小
    for batch_size in batch_sizes:
        # 筛选出当前批量大小的数据
        data = df[df['batch_size'] == batch_size]

        # 将数据存储到字典中
        batch_size_data_dict[batch_size] = data

    return batch_size_data_dict

def plot_batch_size_comparison(batch_size_data_dict, save_path=None, figsize=(12, 8)):
    """
    绘制不同批量大小的性能比较图

    参数:
    batch_size_data_dict: 字典，键为批量大小，值为包含训练数据的DataFrame
                            每个DataFrame应包含列：'epoch', 'train_loss', 'train_accuracy', 'test_accuracy'
    save_path: 字符串，图表保存路径，默认为None（不保存）
    figsize: 元组，图表尺寸

    返回:
    matplotlib图表对象
    """
    plt.figure(figsize=figsize)

    # 绘制训练损失
    plt.subplot(2, 2, 1)
    for batch_size, data in batch_size_data_dict.items():
        plt.plot(data['epoch'], data['train_loss'], label=f'Batch Size={batch_size}')
    plt.xlabel('Epoch')
    plt.ylabel('Training Loss')
    plt.title('Training Loss Comparison')
    plt.legend()

    # 绘制训练准确率
    plt.subplot(2, 2, 2)
    for batch_size, data in batch_size_data_dict.items():
        plt.plot(data['epoch'], data['train_accuracy'], label=f'Batch Size={batch_size}')
    plt.xlabel('Epoch')
    plt.ylabel('Training Accuracy')
    plt.title('Training Accuracy Comparison')
    plt.legend()

    # 绘制测试准确率
    plt.subplot(2, 2, 3)
    for batch_size, data in batch_size_data_dict.items():
        plt.plot(data['epoch'], data['test_accuracy'], label=f'Batch Size={batch_size}')
    plt.xlabel('Epoch')
    plt.ylabel('Test Accuracy')
    plt.title('Test Accuracy Comparison')
    plt.legend()

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)

    plt.show()

# CSV文件路径
file_path = r"./3_different_batch_size.csv"  

# 读取并处理CSV文件
batch_size_data_dict = read_and_process_csv(file_path)

# 调用函数绘制图表
plot_batch_size_comparison(batch_size_data_dict)
