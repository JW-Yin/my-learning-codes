import threading
import queue
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(message)s"
)
logger = logging.getLogger(__name__)

DVWA_COOKIES = {
    "PHPSESSID": "9rt02bki9959h3d6n0qqas30c2",
    "security": "low"
}

# 创建线程安全队列（最多存5个URL）
url_queue = queue.Queue(maxsize=5)

def producer():
    """生产者：往队列放DVWA URL"""
    dvwa_urls = [
        "http://127.0.0.1/dvwa/vulnerabilities/sqli/",
        "http://127.0.0.1/dvwa/vulnerabilities/xss_r/",
        "http://127.0.0.1/dvwa/vulnerabilities/upload/"
    ]
    for url in dvwa_urls:
        url_queue.put(url)
        logger.info(f"放入URL：{url}，队列大小：{url_queue.qsize()}")
    # 放结束标记（None），告诉消费者退出
    for _ in range(2):  # 2个消费者，放2个None
        url_queue.put(None)

def consumer():
    """消费者：从队列取URL爬取"""
    while True:
        url = url_queue.get()  # 阻塞，直到队列有数据
        if url is None:  # 收到结束标记
            logger.info("收到结束标记，退出")
            url_queue.task_done()  # 结束标记也要标记done
            break
        try:
            response = requests.get(url, cookies=DVWA_COOKIES, timeout=5)
            logger.info(f"爬取成功：{url}，长度：{len(response.text)}")
        except Exception as e:
            logger.error(f"爬取失败：{url}，错误：{str(e)}")
        finally:  # 无论成功/失败，都标记任务完成
            url_queue.task_done()

if __name__ == "__main__":
    # 创建线程
    producer_thread = threading.Thread(target=producer, name="Producer")
    consumer1 = threading.Thread(target=consumer, name="Consumer-1")
    consumer2 = threading.Thread(target=consumer, name="Consumer-2")

    # 启动线程
    producer_thread.start()
    consumer1.start()
    consumer2.start()

    # 等待队列所有任务完成
    url_queue.join()
    # 等待线程结束
    producer_thread.join()
    consumer1.join()
    consumer2.join()

    logger.info("所有任务完成！")