import threading
import requests
import logging
import time

# 配置日志（你已掌握的技能，保持熟悉的用法）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"  # 显示线程名，方便观察
)
logger = logging.getLogger(__name__)

# 替换成你的DVWA Cookie
DVWA_COOKIES = {
    "PHPSESSID": "9rt02bki9959h3d6n0qqas30c2",  # 示例：q1234567890abcdef
    "security": "low"
}

# 线程要执行的函数：爬取DVWA页面
def crawl_dvwa_page(url):
    logger.info(f"开始爬取：{url}")
    try:
        # 发请求（IO操作，会触发线程阻塞）
        response = requests.get(url, cookies=DVWA_COOKIES, timeout=5)
        response.raise_for_status()  # 抛出HTTP错误（比如404）
        logger.info(f"爬取成功：{url}，页面长度：{len(response.text)}")
    except Exception as e:
        logger.error(f"爬取失败：{url}，错误：{str(e)}")
    # time.sleep(1)  # 模拟耗时，方便观察线程切换

if __name__ == "__main__":
    # 要爬取的DVWA页面
    dvwa_urls = [
        "http://127.0.0.1/dvwa/vulnerabilities/sqli/",  # SQL注入
        "http://127.0.0.1/dvwa/vulnerabilities/xss_r/"   # 反射型XSS
    ]



    logger.info("开始单线程爬取...")
    crawl_dvwa_page(dvwa_urls[0])  # 单线程测试
    crawl_dvwa_page(dvwa_urls[1])  # 单线程测试
    logger.info("单线程爬取完毕，开始多线程爬取...\n\n")


    # 1. 创建线程（新建状态）
    thread1 = threading.Thread(target=crawl_dvwa_page, args=(dvwa_urls[0],), name="Thread-SQLi")
    thread2 = threading.Thread(target=crawl_dvwa_page, args=(dvwa_urls[1],), name="Thread-XSS")

    # 2. 启动线程（进入就绪状态）
    logger.info("启动线程...")
    thread1.start()
    thread2.start()

    # 3. 等待线程结束（主线程阻塞，避免提前退出）
    thread1.join()
    thread2.join()

    logger.info("所有线程执行完毕！")