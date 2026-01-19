import requests

# 1. 配置信息（改成你自己的DVWA地址）
dvwa_login_url = "http://127.0.0.1/dvwa/login.php"  # 本地DVWA的登录页
dvwa_vuln_url = "http://127.0.0.1/dvwa/vulnerabilities/sqli/"  # SQL注入漏洞页

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
login_data = {"username": "admin", "password": "password", "Login": "Login"}  # DVWA默认账号

try:
    # 2. 发送POST请求登录DVWA
    login_response = requests.post(
        dvwa_login_url,
        data=login_data,
        headers=headers,
        timeout=5  # 超时设置
    )
    # 处理编码，避免中文乱码
    login_response.encoding = login_response.apparent_encoding

    # 3. 提取登录后的Cookie
    login_cookies = login_response.cookies.get_dict()
    print("登录成功，Cookie是：", login_cookies)

    # 4. 带Cookie访问漏洞页面（GET请求）
    vuln_response = requests.get(
        dvwa_vuln_url,
        headers=headers,
        cookies=login_cookies,  # 带登录Cookie
        timeout=5
    )
    vuln_response.encoding = vuln_response.apparent_encoding

    # 5. 查看结果
    print("\n漏洞页面访问状态：", vuln_response.status_code)
    print("漏洞页面内容（前300字）：\n", vuln_response.text[:300])

except Exception as e:
    print("出错了：", e)