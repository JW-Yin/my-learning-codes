import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

test_urls = {
    "正常URL": "https://httpbin.org/get",
    "404 URL": "https://httpbin.org/status/404",# 404错误页面
    "500 URL": "https://httpbin.org/status/500"# 500错误页面
}

for name, url in test_urls.items():
    print(f"\n=== 测试 {name} ===")
    try:
        response = requests.get(url, headers=headers, timeout=5)
        # 核心：raise_for_status() —— 状态码非200时主动抛出异常
        response.raise_for_status()
        print(f"请求成功！响应内容：{response.text[:50]}...")  # 只打印前50个字符
    except requests.exceptions.HTTPError as e:
        # 捕获HTTP错误（4xx/5xx状态码）
        print(f"HTTP错误：{e}")
    except requests.exceptions.Timeout:
        print("请求超时！")
    except Exception as e:
        print(f"未知错误：{e}")