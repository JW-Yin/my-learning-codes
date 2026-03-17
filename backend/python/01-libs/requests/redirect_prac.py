import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 访问http://baidu.com（会自动跳转到https://www.baidu.com）

# ---- 场景1：查看默认的重定向历史 ----
response1 = requests.get(
    "http://baidu.com", 
    headers=headers, 
    timeout=5
)
print("=== 重定向历史（默认自动跳转）===")
print(f"最终响应状态码：{response1.status_code}")
print(f"重定向次数：{len(response1.history)}")  # 历史记录数=重定向次数
for i, redirect in enumerate(response1.history):
    print(f"第{i+1}次重定向：{redirect.url} -> 状态码 {redirect.status_code}")
print(f"最终访问的URL：{response1.url}")

# ---- 场景2：关闭自动重定向 ----
response2 = requests.get(
    "http://baidu.com",
    headers=headers,
    timeout=5,
    allow_redirects=False  # 核心：关闭自动重定向
)
print("\n=== 关闭自动重定向后 ===")
print(f"响应状态码：{response2.status_code}")  # 会返回301（永久重定向状态码）
print(f"是否需要跳转：{response2.is_redirect}")  # True表示需要重定向
print(f"原始URL（未跳转）：{response2.url}")