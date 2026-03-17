import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

count = 0  # 共享变量（统计DVWA漏洞数量的模拟）
lock = threading.Lock()  # 创建锁对象

def increment(use_lock: bool = False):
    """累加count，可选是否加锁"""
    global count
    for _ in range(100000):  # 每个线程累加10万次
        if use_lock:
            # with自动获取/释放锁（推荐，避免死锁）
            with lock:
                count += 1
        else:
            count += 1  # 不加锁，会出现竞态条件

# 测试1：不加锁（预期50万，实际小于50万）
logger.info("===== 测试不加锁 =====")
count = 0
threads = [threading.Thread(target=increment) for _ in range(500)]
for t in threads:
    t.start()
for t in threads:
    t.join()
logger.info(f"不加锁的最终count：{count}")  # 结果≈49900000（随机）

# 测试2：加锁（预期50万，实际=50万）
logger.info("===== 测试加锁 =====")
count = 0
threads = [threading.Thread(target=increment, args=(True,)) for _ in range(500)]
for t in threads:
    t.start()
for t in threads:
    t.join()
logger.info(f"加锁的最终count：{count}")  # 结果=50000000