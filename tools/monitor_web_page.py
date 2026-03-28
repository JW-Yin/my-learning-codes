import requests
import hashlib
import os
import random
import time
from fake_useragent import UserAgent  # 需安装：pip install fake-useragent

# ====================== 配置部分（仅需修改这里） ======================
# 目标网页 URL 列表（把你要监控的所有页面放这里）
TARGET_URLS = [
    "https://www.guet.edu.cn/yjszs/2025/0905/c4230a141350/page.htm",  # 原有的桂电研招通知页
    "https://www.guet.edu.cn/yjszs/4230/list.htm",                        # 通知首页
    "https://www.guet.edu.cn/yjszs/2026/0322/c4230a149911/page.htm",
    "https://www.guet.edu.cn/yjszs/2026/0323/c4245a150076/page.htm" # 拟录取名单
    # 继续添加更多 URL...
]
# 用于存储所有页面哈希值的目录（每个页面对应一个独立文件）
HASH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "page_hashes")
# ======================================================================

# 初始化随机 User-Agent 生成器
ua = UserAgent()

def get_random_headers():
    """生成真人级随机请求头（保持原样）"""
    return {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": random.choice(["zh-CN,zh;q=0.9", "zh;q=0.8,en;q=0.2"]),
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.guet.edu.cn/",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }

def get_page_content(url, retry_count=0):
    """获取网页内容（带指数退避重试，保持原样）"""
    max_retry = 3
    try:
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(
            url, 
            headers=get_random_headers(), 
            timeout=15,
            verify=True,
            stream=True
        )
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.exceptions.ConnectionError as e:
        if retry_count < max_retry:
            wait_time = 10 * (2 ** retry_count)
            print(f"[{url}] 连接失败，{wait_time}秒后重试（第{retry_count+1}次）")
            time.sleep(wait_time)
            return get_page_content(url, retry_count + 1)
        else:
            print(f"[{url}] 获取网页出错（已重试{max_retry}次）: {e}")
            return None
    except requests.RequestException as e:
        print(f"[{url}] 获取网页出错: {e}")
        return None

def compute_hash(content):
    """计算网页内容的 SHA-256 哈希值（保持原样）"""
    sha256 = hashlib.sha256()
    sha256.update(content.encode('utf-8'))
    return sha256.hexdigest()

def get_hash_file_path(url):
    """根据 URL 生成唯一的哈希文件路径（新增核心函数）"""
    # 用 URL 的 SHA-256 哈希值作为文件名，避免特殊字符问题，且保证唯一
    url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
    return os.path.join(HASH_DIR, f"{url_hash}.txt")

def read_old_hash(url):
    """读取指定 URL 本地存储的旧哈希值（适配多页面）"""
    hash_file = get_hash_file_path(url)
    if not os.path.exists(hash_file):
        return None
    with open(hash_file, 'r', encoding='utf-8') as f:
        return f.read().strip()

def save_new_hash(url, hash_value):
    """保存指定 URL 的新哈希值到本地（适配多页面）"""
    # 确保哈希目录存在
    if not os.path.exists(HASH_DIR):
        os.makedirs(HASH_DIR, exist_ok=True)
    hash_file = get_hash_file_path(url)
    with open(hash_file, 'w', encoding='utf-8') as f:
        f.write(hash_value)

def monitor_single_url(url):
    """监控单个 URL 的逻辑（从原 main 函数拆分出来）"""
    print(f"\n正在监控: {url}")
    
    # 1. 获取网页内容
    content = get_page_content(url)
    if content is None:
        print(f"[{url}] 跳过本次监控（获取内容失败）")
        return

    # 2. 计算当前哈希
    current_hash = compute_hash(content)

    # 3. 读取旧哈希
    old_hash = read_old_hash(url)

    if old_hash is None:
        save_new_hash(url, current_hash)
        print(f"[{url}] 首次监控，已记录当前页面状态。")
    else:
        if current_hash != old_hash:
            print(f"⚠️有新更新！")
            save_new_hash(url, current_hash)
            
        else:
            print(f"暂无更新...")

def main():
    print("="*60)
    print(f"开始多页面监控，共 {len(TARGET_URLS)} 个目标")
    print("="*60)
    
    # 循环监控每个 URL
    for url in TARGET_URLS:
        # 请求前随机小延迟（模拟真人打开浏览器的等待）
        time.sleep(random.uniform(1, 3))
        monitor_single_url(url)
    
    print("\n" + "="*60)
    print("本轮监控完成")
    print("="*60)

if __name__ == "__main__":
    main()
