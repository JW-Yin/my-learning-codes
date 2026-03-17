import requests

url = "https://httpbin.org/post"  # 这个网址专门用来测试 POST 请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 1. 定义要提交的表单数据（字典格式）
data = {
    "username": "test小白",
    "password": "123456",
    "age": "20"
}

# 2. 发送 POST 请求，通过 data 参数传入表单数据
response = requests.post(url=url, headers=headers, data=data, timeout=5)
#【解决乱码】自动识别编码
response.encoding = response.apparent_encoding

# 3. 打印结果
print("POST 请求成功，响应内容：")
print(response.json())  # 以 JSON 格式打印响应内容

# 提取响应的 Cookies(转成字典格式，方便后续用)
cookies = response.cookies.get_dict()

# 4. 再次发送 POST 请求，携带上次响应的 Cookies
response = requests.post(url=url, headers=headers, cookies=cookies, data=data, timeout=5)


import requests
headers = {"User-Agent": "你的UA"}
login_data = {"username": "账号", "password": "密码"}

# 普通requests.post的写法
requests.post(
    url="https://网站.com/login",
    headers=headers,
    data=login_data,
    timeout=5
)

# 改成session.post的写法（参数完全一样）
session = requests.Session()
session.post(
    url="https://网站.com/login",
    headers=headers,
    data=login_data,
    timeout=5
)



