#!/usr/bin/env python
# coding: utf-8

# In[50]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from IPython.display import display, Markdown
from IPython.display import display

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 定义数据文件路径 
data_dir = r'E:\穿越火线赛事热度与观众参与度分析\1'
data_dir2 = r'E:\穿越火线赛事热度与观众参与度分析\2' 
data_dir3 = r'E:\穿越火线赛事热度与观众参与度分析\3'
data_dir4 = r'E:\穿越火线赛事热度与观众参与度分析\4'


# 检查路径是否存在
if not os.path.exists(data_dir):
    raise FileNotFoundError(f"指定的数据目录不存在: {data_dir}")
    
    

# 定义数据文件
data_files = {
    'public_opinion': '穿越火线舆情热度数据.xlsx',
    'city_heat': '城市舆情热度TOP30.xlsx',
    'player_comments': '穿越火线玩家评论.xlsx',
    'emoji_data': '表情评论数据.xlsx'
}

# 读取数据函数
def load_data(file_name):
    file_path = os.path.join(data_dir, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    return pd.read_excel(file_path)

# 加载所有数据
try:
    public_opinion = load_data(data_files['public_opinion'])
    city_heat = load_data(data_files['city_heat'])
    player_comments = load_data(data_files['player_comments'])
    emoji_data = load_data(data_files['emoji_data'])
except FileNotFoundError as e:
    print(f"加载数据时出错: {e}")
    print("请检查以下内容:")
    print(f"1. 数据目录是否正确: {data_dir}")
    print(f"2. 目录中是否包含以下文件: {list(data_files.values())}")
    raise

# 数据预览
print("舆情热度数据预览:")
display(public_opinion.head())
print("\n城市热度TOP30预览:")
display(city_heat.head())
print("\n玩家评论数据预览:")
display(player_comments.head())
print("\n表情评论数据预览:")
display(emoji_data.head())


# In[3]:


# 舆情热度趋势分析
plt.figure(figsize=(15, 7))
plt.plot(public_opinion['日期'], public_opinion['舆情热度'], marker='o', linestyle='-', color='#3498db')
plt.title('2018-2022年穿越火线电竞舆情热度趋势', fontsize=16)
plt.xlabel('日期', fontsize=12)
plt.ylabel('舆情热度', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# 标记特殊事件
plt.annotate('十周年活动', xy=('2018/8', 13433182), xytext=('2018/6', 15000000),
             arrowprops=dict(facecolor='red', shrink=0.05))
plt.annotate('网剧上线', xy=('2020/8', 35114142), xytext=('2020/6', 37000000),
             arrowprops=dict(facecolor='red', shrink=0.05))

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 年度舆情总量分析
yearly_data = public_opinion.copy()
yearly_data['年份'] = pd.to_datetime(yearly_data['日期']).dt.year
yearly_sum = yearly_data.groupby('年份')['舆情热度'].sum().reset_index()

plt.figure(figsize=(10, 6))
bars = plt.bar(yearly_sum['年份'], yearly_sum['舆情热度'], color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6'])
plt.title('2018-2022年穿越火线电竞年度舆情总量', fontsize=16)
plt.xlabel('年份', fontsize=12)
plt.ylabel('舆情总量', fontsize=12)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height/10000:.1f}万',
             ha='center', va='bottom')

plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# In[4]:


# 城市热度TOP10
top10_cities = city_heat.sort_values('舆情热度', ascending=False).head(10)

plt.figure(figsize=(12, 6))
bars = plt.barh(top10_cities['城市'], top10_cities['舆情热度'], color=sns.color_palette('viridis', 10))
plt.title('穿越火线电竞舆情热度TOP10城市', fontsize=16)
plt.xlabel('舆情热度', fontsize=12)
plt.ylabel('城市', fontsize=12)

# 添加数据标签
for bar in bars:
    width = bar.get_width()
    plt.text(width + 500, bar.get_y() + bar.get_height()/2,
             f'{width:,}',
             va='center')

plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 城市级别分布
city_level_dist = city_heat['城市级别'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(city_level_dist, labels=city_level_dist.index, autopct='%1.1f%%',
        colors=['#3498db', '#2ecc71', '#e74c3c'], startangle=90)
plt.title('舆情热度TOP30城市级别分布', fontsize=16)
plt.tight_layout()
plt.show()


# In[5]:


# 玩家类型分布
player_type_dist = player_comments['用户类型'].value_counts()

plt.figure(figsize=(10, 6))
bars = plt.bar(player_type_dist.index, player_type_dist, color=sns.color_palette('pastel'))
plt.title('玩家评论用户类型分布', fontsize=16)
plt.xlabel('用户类型', fontsize=12)
plt.ylabel('数量', fontsize=12)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}',
             ha='center', va='bottom')

plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 评论情感关键词提取
keywords = ['十年玩家', '青春', '感动', '初心', '致敬', 'CFS', 'CFer']
keyword_counts = {kw: player_comments['评论内容'].str.contains(kw).sum() for kw in keywords}

plt.figure(figsize=(10, 6))
bars = plt.bar(keyword_counts.keys(), keyword_counts.values(), color='#f39c12')
plt.title('玩家评论高频情感关键词统计', fontsize=16)
plt.xlabel('关键词', fontsize=12)
plt.ylabel('出现次数', fontsize=12)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}',
             ha='center', va='bottom')

plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# In[6]:


# 表情使用频率
emoji_freq = emoji_data['表情'].value_counts()

plt.figure(figsize=(10, 6))
bars = plt.bar(emoji_freq.index, emoji_freq, color=sns.color_palette('Set2'))
plt.title('玩家评论表情使用频率', fontsize=16)
plt.xlabel('表情', fontsize=12)
plt.ylabel('使用次数', fontsize=12)

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}',
             ha='center', va='bottom')

plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 表情占比分析
emoji_percent = emoji_data.groupby('表情')['占比'].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
plt.bar(emoji_percent.index, emoji_percent, color='#9b59b6')
plt.title('各类表情在评论中的平均占比', fontsize=16)
plt.xlabel('表情', fontsize=12)
plt.ylabel('平均占比', fontsize=12)
plt.ylim(0, 0.35)

# 添加数据标签
for i, v in enumerate(emoji_percent):
    plt.text(i, v + 0.01, f"{v:.2f}", ha='center')

plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# In[ ]:





# In[13]:


data_dir2 = r'E:\穿越火线赛事热度与观众参与度分析\2'

# 检查路径是否存在
if not os.path.exists(data_dir2):
    raise FileNotFoundError(f"指定的数据目录不存在: {data_dir2}")
    
# 定义数据文件
audience_data_files = {
    'profile': '观众画像数据.xlsx',
    'behavior': '电竞观众线上娱乐行为数据.xlsx'
}

# 读取数据函数
def load_audience_data():
    try:
        profile_df = pd.read_excel(os.path.join(data_dir2, audience_data_files['profile']))
        behavior_df = pd.read_excel(os.path.join(data_dir2, audience_data_files['behavior']))
        return profile_df, behavior_df
    except FileNotFoundError as e:
        print(f"加载数据时出错: {e}")
        print("请检查以下内容:")
        print(f"1. 数据目录是否正确: {data_dir2}")
        print(f"2. 目录中是否包含以下文件: {list(audience_data_files.values())}")
        raise

# 加载数据
try:
    profile_df, behavior_df = load_audience_data()
    print("数据加载成功！")
except Exception as e:
    print(f"数据加载失败: {e}")
    raise

# 数据预览 - 修正变量名错误
print("\n观众画像数据预览:")
display(profile_df.head(3))
print("\n电竞观众线上娱乐行为数据预览:")
display(behavior_df.head(3))


# In[16]:


#观众画像分析
def analyze_and_visualize(profile_df, behavior_df):
   
    plt.figure(figsize=(18, 6))
    plt.suptitle('CF电竞观众与全国电竞观众画像对比', fontsize=16)
    
    # 计算各类别比例
    cf_gender = profile_df[profile_df['观众类型'] == 'CF电竞观众']['性别'].value_counts(normalize=True) * 100
    national_gender = profile_df[profile_df['观众类型'] == '全国电竞观众']['性别'].value_counts(normalize=True) * 100
    
    cf_age = profile_df[profile_df['观众类型'] == 'CF电竞观众']['年龄段'].value_counts(normalize=True) * 100
    national_age = profile_df[profile_df['观众类型'] == '全国电竞观众']['年龄段'].value_counts(normalize=True) * 100
    
    # 收入分析
    def income_group(income):
        if '8000' in income or '15000' in income:
            return '高收入(8000元以上)'
        elif '6000' in income:
            return '中等收入(3001-6000元)'
        else:
            return '其他收入'
    
    profile_df['收入分组'] = profile_df['收入水平'].apply(income_group)
    cf_income = profile_df[profile_df['观众类型'] == 'CF电竞观众']['收入分组'].value_counts(normalize=True) * 100
    national_income = profile_df[profile_df['观众类型'] == '全国电竞观众']['收入分组'].value_counts(normalize=True) * 100
    
    # 性别对比
    plt.subplot(1, 3, 1)
    gender_df = pd.DataFrame({
        'CF电竞观众': [cf_gender.get('男', 0), cf_gender.get('女', 0)],
        '全国电竞观众': [national_gender.get('男', 0), national_gender.get('女', 0)]
    }, index=['男性', '女性'])
    
    gender_df.plot(kind='bar', color=['#3498db', '#e74c3c'], ax=plt.gca())
    plt.title('性别分布对比(%)', fontsize=12)
    plt.ylabel('比例(%)', fontsize=10)
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 年龄对比
    plt.subplot(1, 3, 2)
    age_order = ['18岁以下', '18-29岁', '30-39岁', '40-49岁', '50-59岁']
    age_df = pd.DataFrame({
        'CF电竞观众': [cf_age.get(age, 0) for age in age_order],
        '全国电竞观众': [national_age.get(age, 0) for age in age_order]
    }, index=age_order)
    
    age_df.plot(kind='bar', color=['#3498db', '#e74c3c'], ax=plt.gca())
    plt.title('年龄分布对比(%)', fontsize=12)
    plt.ylabel('比例(%)', fontsize=10)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 收入对比
    plt.subplot(1, 3, 3)
    income_order = ['高收入(8000元以上)', '中等收入(3001-6000元)', '其他收入']
    income_df = pd.DataFrame({
        'CF电竞观众': [cf_income.get(income, 0) for income in income_order],
        '全国电竞观众': [national_income.get(income, 0) for income in income_order]
    }, index=income_order)
    
    income_df.plot(kind='bar', color=['#3498db', '#e74c3c'], ax=plt.gca())
    plt.title('收入水平对比(%)', fontsize=12)
    plt.ylabel('比例(%)', fontsize=10)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()
    


# 执行分析
analyze_and_visualize(profile_df, behavior_df)


# In[25]:


# 线上娱乐行为分析
plt.figure(figsize=(12, 6))

# 计算CF观众各项活动参与比例
cf_behavior = behavior_df[behavior_df['观众类型'] == 'CF电竞观众']
activity_rates = cf_behavior.groupby('线上活动')['参与比例'].mean().sort_values(ascending=False).head(5)

bars = plt.barh(activity_rates.index, activity_rates, color=sns.color_palette('viridis', 5))
plt.title('CF电竞观众线上娱乐活动TOP5(参与比例%)', fontsize=16)
plt.xlabel('参与比例(%)', fontsize=12)

# 添加数据标签
for bar in bars:
    width = bar.get_width()
    plt.text(width + 0.5, bar.get_y() + bar.get_height()/2,
             f'{width:.1f}%',
             va='center')

plt.grid(True, linestyle='--', alpha=0.7)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

   # 三维总览图
plt.figure(figsize=(14, 8))

# 准备数据 - 使用.copy()避免警告
cf_behavior = behavior_df[behavior_df['观众类型'] == 'CF电竞观众'].copy()
consumption_map = {'低':1, '中':2, '高':3}
cf_behavior['消费数值'] = cf_behavior['月均消费'].map(consumption_map)

activity_stats = cf_behavior.groupby('线上活动').agg({
'参与比例': 'mean',
'日均时长(小时)': 'mean',
'消费数值': 'mean'
}).reset_index()

scatter = plt.scatter(
x=activity_stats['日均时长(小时)'],
y=activity_stats['参与比例']*100,
s=activity_stats['消费数值']*100,
c=activity_stats['消费数值'],
cmap='viridis',
alpha=0.7
)

# 添加标签
for i, row in activity_stats.iterrows():
    plt.text(
        x=row['日均时长(小时)']+0.02,
        y=row['参与比例']*100+1,
        s=row['线上活动'],
        fontsize=9
    )

# 设置图表元素
plt.title('CF电竞观众线上娱乐活动三维总览', fontsize=16)
plt.xlabel('日均时长(小时)', fontsize=12)
plt.ylabel('参与比例(%)', fontsize=12)
cbar = plt.colorbar(scatter)
cbar.set_label('消费水平(低=1,中=2,高=3)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()




# In[27]:


data_dir3 = r'E:\穿越火线赛事热度与观众参与度分析\3'

if not os.path.exists(data_dir3):
    raise FileNotFoundError(f"指定的数据目录不存在: {data_dir3}")

data_files = {
    'viewing_behavior': '电竞观众观赛行为数据.xlsx',
    'live_attendance': '电竞观众现场观赛数据.xlsx',
    'viewing_willingness': '电竞观众观赛意愿数据.xlsx'
}

# 读取数据函数
def load_data(file_name):
    file_path = os.path.join(data_dir3, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    return pd.read_excel(file_path)

# 加载所有数据
try:
    viewing_behavior = load_data(data_files['viewing_behavior'])
    live_attendance = load_data(data_files['live_attendance'])
    viewing_willingness = load_data(data_files['viewing_willingness'])
except FileNotFoundError as e:
    print(f"加载数据时出错: {e}")
    print("请检查以下内容:")
    print(f"1. 数据目录是否正确: {data_dir3}")
    print(f"2. 目录中是否包含以下文件: {list(data_files.values())}")
    raise

# 数据预览
print("观赛行为数据预览:")
display(viewing_behavior.head())
print("\n现场观赛数据预览:")
display(live_attendance.head())
print("\n观赛意愿数据预览:")
display(viewing_willingness.head())



# In[58]:


# 观赛频率时长分析（赛事周期 vs 休赛期）
def analyze_and_visualize(viewing_behavior, live_attendance, viewing_willingness):
   # CF电竞观众数据
   cf_data = viewing_behavior[viewing_behavior['观众类型'] == 'CF电竞观众']
   
   # 赛事周期数据
   cf_season = cf_data[cf_data['时期'] == '赛事周期']
   
   # 休赛期数据
   cf_offseason = cf_data[cf_data['时期'] == '休赛期内']
   
   # 现场观赛数据
   valid_attendance = live_attendance[live_attendance['现场观赛'] == '是']
   cf_attendance = valid_attendance[valid_attendance['观众类型'] == 'CF电竞观众']
   national_attendance = valid_attendance[valid_attendance['观众类型'] == '全国电竞观众']
   
   # 观赛意愿数据
   cf_willingness = viewing_willingness[viewing_willingness['观众类型'] == 'CF电竞观众']
   national_willingness = viewing_willingness[viewing_willingness['观众类型'] == '全国电竞观众']

   # 观赛频率分析（赛事周期 vs 休赛期）
   plt.figure(figsize=(16, 6))
   plt.suptitle('CF电竞观众观赛频率对比（赛事周期 vs 休赛期）', fontsize=16)
   
   # 赛事周期观赛频率
   plt.subplot(1, 2, 1)
   freq_counts = cf_season['观赛频率'].value_counts(normalize=True).sort_values(ascending=False) * 100
   bars = freq_counts.plot(kind='bar', color=sns.color_palette('Blues'))
   plt.title('赛事周期观赛频率(%)', fontsize=12)
   plt.ylabel('比例(%)', fontsize=10)
   plt.xticks(rotation=45)
   
   for bar in bars.patches:
       height = bar.get_height()
       plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
   
   # 休赛期观赛频率
   plt.subplot(1, 2, 2)
   freq_counts = cf_offseason['观赛频率'].value_counts(normalize=True).sort_values(ascending=False) * 100
   bars = freq_counts.plot(kind='bar', color=sns.color_palette('Reds'))
   plt.title('休赛期观赛频率(%)', fontsize=12)
   plt.ylabel('比例(%)', fontsize=10)
   plt.xticks(rotation=45)
   
   for bar in bars.patches:
       height = bar.get_height()
       plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
   
   plt.tight_layout()
   plt.show()
   
   #  观赛时长分析
   plt.figure(figsize=(14, 6))
   
   
   # CF观众赛事周期时长分布
   plt.subplot(1, 2, 1)
   cf_season_duration = cf_season['观赛时长'].value_counts(normalize=True) * 100
   bars = cf_season_duration.plot(kind='bar', color=sns.color_palette('Blues'))
   plt.title('CF观众赛事周期观赛时长分布(%)', fontsize=12)
   plt.ylabel('比例(%)', fontsize=10)
   plt.xticks(rotation=45)
   
   for bar in bars.patches:
       height = bar.get_height()
       plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
   
   # CF观众休赛期时长分布
   plt.subplot(1, 2, 2)
   cf_offseason_duration = cf_offseason['观赛时长'].value_counts(normalize=True) * 100
   bars = cf_offseason_duration.plot(kind='bar', color=sns.color_palette('Reds'))
   plt.title('CF观众休赛期观赛时长分布(%)', fontsize=12)
   plt.ylabel('比例(%)', fontsize=10)
   plt.xticks(rotation=45)
   
   for bar in bars.patches:
       height = bar.get_height()
       plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom')
   
   plt.tight_layout()
   plt.show()

# 执行分析
analyze_and_visualize(viewing_behavior, live_attendance, viewing_willingness)


# In[55]:


# 现场观赛情况分析
plt.figure(figsize=(12, 6))

# 观赛场次对比
plt.subplot(1, 2, 1)
cf_counts = cf_attendance['观赛场次'].value_counts(normalize=True) * 100
national_counts = national_attendance['观赛场次'].value_counts(normalize=True) * 100

df = pd.DataFrame({
    'CF电竞观众': cf_counts,
    '全国电竞观众': national_counts
}).fillna(0)

df.plot(kind='bar', color=['#3498db', '#e74c3c'], ax=plt.gca())
plt.title('现场观赛场次对比(%)', fontsize=12)
plt.ylabel('比例(%)', fontsize=10)
plt.xticks(rotation=0)


# In[56]:


# 观赛意愿分析
plt.subplot(1, 2, 2)
cf_counts = cf_willingness['观赛意愿'].value_counts(normalize=True) * 100
national_counts = national_willingness['观赛意愿'].value_counts(normalize=True) * 100

df = pd.DataFrame({
    'CF电竞观众': cf_counts,
    '全国电竞观众': national_counts
}).fillna(0)

df.plot(kind='bar', color=['#3498db', '#e74c3c'], ax=plt.gca())
plt.title('观赛意愿对比(%)', fontsize=12)
plt.ylabel('比例(%)', fontsize=10)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()



# In[63]:


data_dir4 = r'E:\穿越火线赛事热度与观众参与度分析\4'

if not os.path.exists(data_dir4):
    raise FileNotFoundError(f"指定的数据目录不存在: {data_dir4}")

# 读取消费行为数据
def load_consumption_data():
    try:
        consumption_path = os.path.join(data_dir4, '穿越火线消费行为分析.xlsx')
        consumption_df = pd.read_excel(consumption_path, sheet_name='消费行为数据')
        return consumption_df
    except Exception as e:
        print(f"加载消费行为数据时出错: {e}")
        raise

# 加载数据
try:
    consumption_df = load_consumption_data()
    print("消费行为数据加载成功！")
except Exception as e:
    print(f"数据加载失败: {e}")
    raise

# 数据清洗和处理
# 去除重复的标题行（假设数据从第3行开始）
consumption_df = consumption_df.iloc[2:].copy()
consumption_df.columns = ['序号', '消费项目', '全国电竞观众', 'CF电竞观众', '差异']

# 转换为数值型
consumption_df['全国电竞观众'] = pd.to_numeric(consumption_df['全国电竞观众'], errors='coerce')
consumption_df['CF电竞观众'] = pd.to_numeric(consumption_df['CF电竞观众'], errors='coerce')
consumption_df['差异'] = pd.to_numeric(consumption_df['差异'], errors='coerce')

# 去除空行
consumption_df = consumption_df.dropna(subset=['消费项目'])

# 数据预览
print("\n消费行为数据预览:")
display(consumption_df.head())



# In[64]:


# 数据分析与可视化
def analyze_consumption(consumption_df):
    # 1. 计算平均消费占比
    display(Markdown("## 消费项目平均占比对比"))
    
    avg_consumption = consumption_df.groupby('消费项目')[['全国电竞观众', 'CF电竞观众']].mean()
    avg_consumption['差异'] = avg_consumption['CF电竞观众'] - avg_consumption['全国电竞观众']
    display(avg_consumption.sort_values('差异', ascending=False))

    # 2. 消费占比TOP5对比
    display(Markdown("## 图一：CF与全国电竞观众消费占比TOP5对比"))
    
    top5_cf = avg_consumption.sort_values('CF电竞观众', ascending=False).head(5)
    top5_national = avg_consumption.sort_values('全国电竞观众', ascending=False).head(5)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    top5_cf['CF电竞观众'].sort_values().plot(kind='barh', ax=axes[0], color='#3498db')
    axes[0].set_title('CF电竞观众消费TOP5')
    axes[0].set_xlabel('消费占比(%)')
    
    top5_national['全国电竞观众'].sort_values().plot(kind='barh', ax=axes[1], color='#e74c3c')
    axes[1].set_title('全国电竞观众消费TOP5')
    axes[1].set_xlabel('消费占比(%)')
    
    plt.tight_layout()
    plt.show()

    # 3. 消费差异分析
    display(Markdown("## 图二：CF与全国电竞观众消费差异TOP10"))
    
    diff_top10 = avg_consumption.sort_values('差异', ascending=False).head(10)
    
    plt.figure(figsize=(12, 6))
    plt.barh(diff_top10.index, diff_top10['差异'], color='#2ecc71')
    plt.title('CF与全国电竞观众消费差异TOP10(CF占比-全国占比)')
    plt.xlabel('消费占比差异(%)')
    plt.grid(axis='x', alpha=0.3)
    plt.show()

    # 4. 消费项目聚类分析
    display(Markdown("## 图三：消费项目聚类分析"))
    
    # 选择主要消费项目
    main_items = avg_consumption[avg_consumption['全国电竞观众'] > 5]  # 过滤掉占比太小的项目
    
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(
        x=main_items['全国电竞观众'],
        y=main_items['CF电竞观众'],
        s=main_items['CF电竞观众']*5,  # 气泡大小表示CF观众消费占比
        c=main_items['差异'],
        cmap='coolwarm',
        alpha=0.7
    )
    
    # 添加标签
    for item in main_items.index:
        plt.text(
            x=main_items.loc[item, '全国电竞观众']+0.5,
            y=main_items.loc[item, 'CF电竞观众']+0.5,
            s=item,
            fontsize=9
        )
    
    # 设置图表元素
    plt.title('消费项目聚类分析')
    plt.xlabel('全国电竞观众消费占比(%)')
    plt.ylabel('CF电竞观众消费占比(%)')
    plt.colorbar(scatter, label='消费占比差异(CF-全国)')
    
    # 添加参考线
    max_val = main_items[['全国电竞观众', 'CF电竞观众']].max().max()
    plt.plot([0, max_val], [0, max_val], '--', color='gray', alpha=0.5)
    plt.text(max_val-5, max_val-2, 'y=x参考线', color='gray')
    
    plt.grid(True, alpha=0.3)
    plt.show()

# 执行分析
analyze_consumption(consumption_df)


# In[ ]:




