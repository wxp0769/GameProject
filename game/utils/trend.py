import matplotlib.pyplot as plt
import pandas as pd
from pytrends.request import TrendReq

# 初始化 Google Trends API
pytrends = TrendReq(hl='en-US', tz=360)

# 设置搜索关键词（可自定义）
kw_list = [ "Drift Boss", "gpts",]

# 选择时间范围（最近 7 天 或 30 天）
time_options = {
    "7d": "now 7-d",  # 过去 7 天
    "30d": "today 1-m"  # 过去 30 天
}

# 用户选择时间范围
selected_timeframe = "30d"  # 改为 "30d" 获取过去 30 天数据

# 构建请求
pytrends.build_payload(kw_list, cat=0, timeframe=time_options[selected_timeframe], geo="", gprop="")

# 获取趋势数据
data = pytrends.interest_over_time()

# 移除 'isPartial' 列（如果存在）
if "isPartial" in data.columns:
    data = data.drop(columns=["isPartial"])

# 绘制趋势曲线
plt.figure(figsize=(12, 6))
for keyword in kw_list:
    plt.plot(data.index, data[keyword], label=keyword, linewidth=2)

# 设置图表标题和标签
plt.title(f"Google Trends Comparison ({selected_timeframe})", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Trend Score", fontsize=12)
plt.legend(title="Keywords")
plt.grid(True, linestyle="--", alpha=0.5)

# 旋转 x 轴日期标签
plt.xticks(rotation=45)

# 显示图表
plt.show()
