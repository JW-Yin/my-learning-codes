import requests
import hashlib
import os
import random
import time
from fake_useragent import UserAgent  # 需安装：pip install fake-useragent

# 目标网页 URL
TARGET_URL = "https://www.guet.edu.cn/yjszs/2025/0905/c4230a141350/page.htm"
# 用于存储上次哈希值的文件
HASH_FILE = "/home/jw-yin/00-my_scripts/monitor_web_page/page_hash.txt"

# 初始化随机 User-Agent 生成器
ua = UserAgent()

def get_random_headers():
    """生成真人级随机请求头"""
    return {
        "User-Agent": ua.random,  # 每次请求换不同的浏览器UA
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": random.choice(["zh-CN,zh;q=0.9", "zh;q=0.8,en;q=0.2"]),
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.guet.edu.cn/",  # 模拟从官网首页点击进入
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        # 增加真人浏览的冗余头，降低特征识别
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }

def get_page_content(url, retry_count=0):
    """获取网页内容（带指数退避重试）"""
    max_retry = 3
    try:
        # 1. 请求前随机小延迟（模拟真人打开浏览器的等待）
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(
            url, 
            headers=get_random_headers(), 
            timeout=15,
            verify=True,
            stream=True  # 流式下载，降低单次请求资源占用
        )
        response.raise_for_status()
        # 自动检测并设置编码，防止中文乱码
        response.encoding = response.apparent_encoding
        return response.text
    except requests.exceptions.ConnectionError as e:
        if retry_count < max_retry:
            # 指数退避重试：10s → 20s → 40s
            wait_time = 10 * (2 ** retry_count)
            print(f"连接失败，{wait_time}秒后重试（第{retry_count+1}次）")
            time.sleep(wait_time)
            return get_page_content(url, retry_count + 1)
        else:
            print(f"获取网页出错（已重试{max_retry}次）: {e}")
            return None
    except requests.RequestException as e:
        print(f"获取网页出错: {e}")
        return None

def compute_hash(content):
    """计算网页内容的 SHA-256 哈希值"""
    sha256 = hashlib.sha256()
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

    # print(content)
    # 2. 计算当前哈希
    current_hash = compute_hash(content)

    # 3. 读取旧哈希
    old_hash = read_old_hash()

    if old_hash is None:
        save_new_hash(current_hash)
        print("首次监控，已记录当前页面状态。")
    else:
        if current_hash != old_hash:
            print("有新更新！")
            save_new_hash(current_hash)
        else:
            print("请等待更新...")

if __name__ == "__main__":
    main()
