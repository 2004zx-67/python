#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from IPython.display import display

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义数据文件路径
base_path = r'E:\穿越火线赛事热度与观众参与度分析'
data_files = {
    'folder1': ['穿越火线舆情热度数据.xlsx', '穿越火线玩家评论.xlsx', '城市舆情热度TOP30.xlsx', '表情评论数据.xlsx'],
    'folder2': ['观众画像数据.xlsx', '电竞观众线上娱乐行为数据.xlsx'],
    'folder3': ['电竞观众观赛意愿数据.xlsx', '电竞观众观赛行为数据.xlsx', '电竞观众现场观赛数据.xlsx'],
    'folder4': ['穿越火线消费行为分析.xlsx']
}

def analyze_dataset(df, name):
    print(f"\n=== {name} 数据集分析 ===")
    
    # 1. 基本情况展示
    print("\n[1] 数据集基本情况")
    print("\n前5行数据:")
    display(df.head())
    
    print("\n数据描述统计:")
    display(df.describe(include='all'))
    
    print("\n数据类型信息:")
    display(pd.DataFrame({
        '列名': df.columns,
        '类型': df.dtypes,
        '非空值数': df.count(),
        '缺失值数': df.isnull().sum()
    }))
    
    # 2. 缺失值处理
    print("\n[2] 缺失值处理")
    print("处理前缺失值统计:")
    display(df.isnull().sum().to_frame('缺失值数'))
    
    # 填充缺失值
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype == 'object':
                df[col].fillna("无", inplace=True)
                print(f"列 '{col}' 的缺失值已用'无'填充")
            else:
                df[col].fillna(0, inplace=True)
                print(f"列 '{col}' 的缺失值已用0填充")
    
    print("\n处理后缺失值统计:")
    display(df.isnull().sum().to_frame('缺失值数'))
    
    # 3. 异常值分析（仅标记不修改）
    print("\n[3] 异常值分析（仅标记不修改）")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    if len(numeric_cols) > 0:
        # 创建异常值标记列
        for col in numeric_cols:
            df[f'{col}_异常值'] = False
        
        # 可视化设置
        plt.figure(figsize=(15, 5*len(numeric_cols)))
        
        for i, col in enumerate(numeric_cols, 1):
            # 计算IQR范围
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5*IQR
            upper_bound = Q3 + 1.5*IQR
            
            # 标记异常值（不修改原值）
            df.loc[(df[col] < lower_bound) | (df[col] > upper_bound), f'{col}_异常值'] = True
            outliers = df[df[f'{col}_异常值']]
            
            # 绘制分布图
            plt.subplot(len(numeric_cols), 2, 2*i-1)
            sns.histplot(df[col], kde=True, color='skyblue')
            plt.title(f'{col}分布')
            plt.axvline(lower_bound, color='r', linestyle='--', label='异常值边界')
            plt.axvline(upper_bound, color='r', linestyle='--')
            if not outliers.empty:
                for x in outliers[col].unique():
                    plt.axvline(x, color='orange', linestyle=':', alpha=0.5)
            plt.legend()
            
            # 绘制箱线图
            plt.subplot(len(numeric_cols), 2, 2*i)
            sns.boxplot(y=df[col], color='lightgreen')
            plt.title(f'{col}箱线图')
        
        plt.tight_layout()
        plt.show()
        
        # 显示异常值详情
        print("\n异常值统计报告:")
        outlier_report = []
        for col in numeric_cols:
            outlier_count = df[f'{col}_异常值'].sum()
            if outlier_count > 0:
                outlier_stats = df[df[f'{col}_异常值']][col].describe().round(2)
                outlier_report.append({
                    '列名': col,
                    '异常值数量': outlier_count,
                    '占比': f"{outlier_count/len(df):.2%}",
                    '最小值': outlier_stats['min'],
                    '最大值': outlier_stats['max'],
                    '平均值': outlier_stats['mean']
                })
                
                print(f"\n{col}异常值详情（共{outlier_count}个，占比{outlier_count/len(df):.2%}）:")
                display(df[df[f'{col}_异常值']].head())
        
        if outlier_report:
            print("\n异常值汇总:")
            display(pd.DataFrame(outlier_report))
        else:
            print("没有检测到异常值")
    else:
        print("没有数值型列可进行异常值分析")
    
    return df

# 主处理流程
processed_data = {}

try:
    for folder, files in data_files.items():
        folder_num = folder.replace('folder', '')
        folder_path = os.path.join(base_path, folder_num)
        print(f"\n{'='*50}\n正在处理目录: {folder_path}\n{'='*50}")
        
        for file in files:
            full_path = os.path.join(folder_path, file)
            if os.path.exists(full_path):
                print(f"\n{'='*30}\n处理文件: {file}\n{'='*30}")
                df = pd.read_excel(full_path)
                processed_df = analyze_dataset(df, file)
                processed_data[file] = processed_df
            else:
                print(f"⚠️ 文件 {file} 不存在，跳过处理")
    
    # 保存处理结果（包含异常值标记）
    output_folder = os.path.join(base_path, 'processed_data_with_outliers')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name, df in processed_data.items():
        output_path = os.path.join(output_folder, 'marked_'+file_name)
        df.to_excel(output_path, index=False)
        print(f"\n✅ 处理后的数据已保存到: {output_path}")
    
    print("\n所有文件处理完成！")
    
except Exception as e:
    print(f"❌ 发生错误: {str(e)}")


# In[ ]:




