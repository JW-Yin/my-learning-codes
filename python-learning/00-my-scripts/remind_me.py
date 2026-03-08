# 当一个网站的内容发生变化时，提醒我。
# 这个脚本会定期检查指定网页的内容，并在检测到变化时输出提示信息。
# 它使用哈希值来比较当前网页内容与上次记录的内容，以确定是否有更新。


import requests
import hashlib
import os

# 目标网页 URL
TARGET_URL = "https://www.guet.edu.cn/yjszs/2025/0905/c4230a141350/page.htm"
# 用于存储上次哈希值的文件
HASH_FILE = "page_hash.txt"

def get_page_content(url):
    """获取网页内容"""
    # 模拟浏览器请求头，防止被反爬拦截
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # 如果请求失败（如404, 500），抛出异常
        # 自动检测并设置编码，防止中文乱码
        response.encoding = response.apparent_encoding
        # print(response.text)  # 输出网页内容，供调试使用
        return response.text
    except requests.RequestException as e:
        print(f"获取网页出错: {e}")
        return None

def compute_hash(content):
    """计算网页内容的 SHA-256 哈希值"""
    sha256 = hashlib.sha256()
    # 必须编码为字节才能计算哈希
    sha256.update(content.encode('utf-8'))
    return sha256.hexdigest()

def read_old_hash():
    """读取本地存储的旧哈希值"""
    if not os.path.exists(HASH_FILE):
        return None
    with open(HASH_FILE, 'r', encoding='utf-8') as f:
        return f.read().strip()

def save_new_hash(hash_value):
    """保存新的哈希值到本地"""
    with open(HASH_FILE, 'w', encoding='utf-8') as f:
        f.write(hash_value)

def main():
    # 1. 获取网页内容
    content = get_page_content(TARGET_URL)
    if content is None:
        return

    # 2. 计算当前哈希
    current_hash = compute_hash(content)

    # 3. 读取旧哈希
    old_hash = read_old_hash()

    if old_hash is None:
        # 第一次运行
        save_new_hash(current_hash)
        print("首次监控，已记录当前页面状态。")
    else:
        if current_hash != old_hash:
            print("有新更新！")
            # 更新哈希值以便下次对比
            save_new_hash(current_hash)
        else:
            print("请等待更新...")

if __name__ == "__main__":
    main()
