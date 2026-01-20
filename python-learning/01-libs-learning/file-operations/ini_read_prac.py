# 导入configparser模块
import configparser
import os
pwd = os.path.abspath(os.path.dirname(__file__))

# 1. 创建ConfigParser对象（配置解析器）
config = configparser.ConfigParser()

# 2. 加载INI配置文件
# 参数1：配置文件路径（和当前py文件同目录，直接写文件名即可）
# 参数2：encoding="utf-8"，指定编码格式，避免中文注释/配置乱码
config.read(pwd+"/config.ini", encoding="utf-8")

# 3. 读取配置值 - 类型安全方法（getint/getboolean/getfloat）

# 读取整数类型：timeout
default_timeout_int = config.getint("DEFAULT", "timeout")
# 读取布尔类型：enable_proxy
enable_proxy_bool = config.getboolean("Proxy", "enable_proxy")

# 打印结果（对应类型）
print("方式2：类型安全方法（自动转换类型）")
print(f"默认超时时间（整数）：{default_timeout_int}，类型：{type(default_timeout_int)}")
print(f"是否启用代理（布尔）：{enable_proxy_bool}，类型：{type(enable_proxy_bool)}")
print("=" * 50)