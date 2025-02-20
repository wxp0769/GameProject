import os

import requests
import re
import json
def get_pic(picurl):

    # 发送请求获取网页内容
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(picurl, headers=headers)
    # 目标存储路径
    save_dir = r"D:\Downloads\pic"
    os.makedirs(save_dir, exist_ok=True)  # 创建目录（如果不存在）
    # 检查请求是否成功
    if response.status_code == 200:
        page_content = response.text

        # 使用正则表达式查找 "thumbnail" 相关的数据
        match = re.search(r'"thumbnail":"(.*?)"', page_content)

        if match:
            thumbnail_path = match.group(1)
            full_thumbnail_url = f"https://imgs.crazygames.com/{thumbnail_path}"
            img_name = thumbnail_path.split("/")[0].split('_')[0] +".png"

            # 下载图片
            img_data = requests.get(full_thumbnail_url, headers=headers).content
            img_name = os.path.join(save_dir, img_name)
            # 保存图片
            with open(img_name, "wb") as f:
                f.write(img_data)
            print("缩略图URL:", full_thumbnail_url)
            print(f"下载路径 {img_name}")
        else:
            print("未找到缩略图")
    else:
        print("无法访问页面，状态码:", response.status_code)
