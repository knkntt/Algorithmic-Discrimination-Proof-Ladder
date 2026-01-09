import pandas as pd

def load_adult_data():
    """
    加载经典的 Adult Dataset (UCI)
    """
    # 这里可以内置一个小型的 csv 采样文件或者通过 URL 下载
    print("正在加载 Adult Dataset...")
    # 模拟返回：数据框, 标签, 敏感属性列名
    mock_data = pd.DataFrame({'age': [25, 45], 'education': [12, 16]})
    mock_target = [0, 1]
    sensitive_attr = 'sex'
    return mock_data, mock_target, sensitive_attr