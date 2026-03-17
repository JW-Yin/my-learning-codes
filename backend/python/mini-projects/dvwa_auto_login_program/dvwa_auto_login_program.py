import requests
from bs4 import BeautifulSoup

def dvwa_auto_login(dvwa_base_url, username, password):
    """
    DVWA自动登录函数，返回保持登录状态的Session对象
    :param dvwa_base_url: DVWA基础地址（如http://127.0.0.1/dvwa）
    :param username: 登录用户名
    :param password: 登录密码
    :return: 已登录的Session对象 / None（登录失败）
    """
    try:
        # 1. 初始化Session对象
        session = requests.Session()
        # 可选：设置请求头，模拟浏览器访问（避免被服务器识别为爬虫）
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        # 2. （可选但推荐）先访问DVWA首页，获取初始Cookie（部分环境需要）
        response=session.get(f"{dvwa_base_url}/")
        # print(response.status_code)
        # print(response.text)

        # 解析登录页HTML，提取user_token
        soup = BeautifulSoup(response.text, "html.parser")
        #user_token = soup.find("input", {"name": "user_token"})["value"]  # 提取隐藏域的user_token值
        user_token = soup.select_one('input[name="user_token"]')["value"]
        # 3. 构造登录表单数据（严格对应DVWA登录页面的表单字段）
        login_data = {
            "username": username,
            "password": password,
            "user_token": user_token, 
            "Login": "Login"
        }

        # 4. 发送登录请求（Session自动保存Cookie）
        login_url = f"{dvwa_base_url}/login.php"
        login_response = session.post(login_url, data=login_data, allow_redirects=True)
        # print(login_response.status_code)
        # print(login_response.text)
        # 5. 验证登录是否成功（通过访问首页，判断是否包含登录后的特征内容）
        index_url = f"{dvwa_base_url}/index.php"
        index_response = session.get(index_url)
        # print(index_response.status_code)
        # print(index_response.text)

        if "Welcome to DVWA" in index_response.text or "DVWA Security" in index_response.text:
            print("DVWA自动登录成功！")
            return session
        else:
            print("DVWA自动登录失败，账号密码或环境配置有误")
            return None

    except Exception as e:
        print(f"登录过程出现异常：{str(e)}")
        return None

# 调用函数执行自动登录
if __name__ == "__main__":
    DVWA_BASE_URL = "http://127.0.0.1/dvwa"
    USERNAME = "admin"
    PASSWORD = "password"
    logged_in_session = dvwa_auto_login(DVWA_BASE_URL, USERNAME, PASSWORD)

    # 登录成功后，可通过该Session对象执行后续自动化操作（如访问漏洞页面、提交测试数据）
    if logged_in_session:
        # 示例：访问SQL注入漏洞页面
        sql_inject_response = logged_in_session.get(f"{DVWA_BASE_URL}/vulnerabilities/sqli/")
        print(f"\n已访问SQL注入页面，页面长度：{len(sql_inject_response.text)}")