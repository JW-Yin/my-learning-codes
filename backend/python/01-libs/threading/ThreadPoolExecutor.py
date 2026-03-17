from concurrent.futures import ThreadPoolExecutor
import requests
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DVWA_COOKIES = {
    "PHPSESSID": "9rt02bki9959h3d6n0qqas30c2",
    "security": "low"
}

# 要检测的DVWA URL列表
DVWA_URLS = [
    "http://127.0.0.1/dvwa/vulnerabilities/sqli/",
    "http://127.0.0.1/dvwa/vulnerabilities/xss_r/",
    "http://127.0.0.1/dvwa/vulnerabilities/upload/"
]

def check_dvwa_url(url):
    """检测URL是否可访问"""
    time.sleep(0.5)  # 避免请求过快
    try:
        response = requests.get(url, cookies=DVWA_COOKIES, timeout=5)
        response.raise_for_status()
        return (url, "成功", f"状态码：{response.status_code}")
    except Exception as e:
        return (url, "失败", str(e))

if __name__ == "__main__":
    # 创建线程池（max_workers=3，IO密集型合适）
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 批量执行任务，返回结果迭代器
        results = executor.map(check_dvwa_url, DVWA_URLS)
        # 遍历结果
        for url, status, msg in results:
            logger.info(f"[{status}] {url} → {msg}")

    logger.info("所有检测完成！")