import requests
from bs4 import BeautifulSoup

# 1. 初始化Session对象
session = requests.Session()
# 设置请求头（模拟浏览器）
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

# 2. 访问登录页，获取初始Cookie和user_token（核心：提取CSRF令牌）
login_page_url = "http://127.0.0.1/dvwa/login.php"
response1 = session.get(login_page_url)

# 解析登录页HTML，提取user_token
soup = BeautifulSoup(response1.text, "html.parser")
user_token = soup.find("input", {"name": "user_token"})["value"]  # 提取隐藏域的user_token值

# 3. 构造完整登录表单（包含user_token，缺一不可）
login_data = {
    "username": "admin",
    "password": "password",
    "user_token": user_token,  # 新增：携带CSRF令牌
    "Login": "Login"
}

# 4. 发送登录请求
login_response = session.post(login_page_url, data=login_data)

# 5. 验证登录状态
index_response = session.get("http://127.0.0.1/dvwa/index.php")
print("index.php 状态码：", index_response.status_code)
print("是否保持登录状态：", "Welcome" in index_response.text)