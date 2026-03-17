# 导入logging模块
import logging
import os
pwd = os.path.abspath(os.path.dirname(__file__))

# 1. 创建Logger对象（日志器），指定日志器名称（推荐使用模块名，这里用项目名）
logger = logging.getLogger("logging的demo")
# 设置Logger的最低日志级别（DEBUG，让所有级别日志都能被传递到Handler）
logger.setLevel(logging.DEBUG)

# 2. 创建Handler对象（处理器）
# 2.1 创建StreamHandler：日志输出到控制台
stream_handler = logging.StreamHandler()
# 设置StreamHandler的日志级别（INFO，可选，这里只输出INFO及以上级别到控制台）
stream_handler.setLevel(logging.INFO)

# 2.2 创建FileHandler：日志输出到文件
file_handler = logging.FileHandler(pwd+"/download.log", encoding="utf-8")
# 设置FileHandler的日志级别（DEBUG，可选，将所有级别日志写入文件，方便调试）
file_handler.setLevel(logging.DEBUG)

# 3. 创建Formatter对象（格式器），定义日志输出格式
log_formatter = logging.Formatter(
    #日志格式中的常用占位符：
    # %(asctime)s（时间）、%(name)s（日志器名称）、%(levelname)s（日志级别）、%(message)s（日志内容）
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 4. 将Formatter绑定到两个Handler（每个Handler可以绑定不同的Formatter，这里用统一格式）
stream_handler.setFormatter(log_formatter)
file_handler.setFormatter(log_formatter)

# 5. 将两个Handler添加到Logger对象中（Logger可以添加多个Handler，实现多端输出）
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# 6. 输出不同级别的日志（使用logger对象调用，而非logging模块直接调用）
logger.debug("这是DEBUG级别的日志（仅写入download.log，控制台不输出）")
logger.info("这是INFO级别的日志（控制台输出+写入download.log）")
logger.warning("这是WARNING级别的日志（控制台输出+写入download.log）")
logger.error("这是ERROR级别的日志（控制台输出+写入download.log）")
logger.critical("这是CRITICAL级别的日志（控制台输出+写入download.log）")