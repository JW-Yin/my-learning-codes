import requests

url = "https://baidu.com"

# 假装浏览器发送请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    # 发送GET请求(携带请求头（headers）、设置超时时间（timeout）)
    response = requests.get(url=url, headers=headers,timeout=10)  
    #【解决乱码】自动识别编码
    response.encoding = response.apparent_encoding

    print("请求成功，状态码：", response.status_code)
    print("\n网页文本内容：\n", response.text[:500])  # 只打印前500个字符
except requests.exceptions.Timeout:
    print("请求超时了！目标网站响应太慢或无法访问")


