import requests
from typing import Optional  # 新增这一行，兼容Python 3.9

# ===================== 配置区域 =====================
EMAIL = "926115191@qq.com"
# 直接填入抓包抓到的那个加密后的密码字符串
ENCRYPTED_PASSWORD = "b6bd42f5fb05e992cf30cf271f892875"

# 地址配置
FRONT_BASE_URL = "http://166.88.141.128:8089"
API_BASE_URL = "http://120.241.238.148:8889"
# ====================================================

# 初始化会话
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Origin": FRONT_BASE_URL,
    "Referer": f"{FRONT_BASE_URL}/",
    "Accept": "application/json",
    "Content-Type": "application/json"
})

# 把这里的 str | None 改成 Optional[str]
def login() -> Optional[str]:
    print("[步骤1] 正在登录...")
    
    # 直接使用加密后的密码
    login_payload = {
        "email": EMAIL,
        "password": ENCRYPTED_PASSWORD
    }

    login_params = {
        "platform": "web",
        "cur_version": "0.0.0",
        "token": "",
        "deviceinfo": "",
        "lang": "hk",
        "code": "Others"
    }

    try:
        resp = session.post(
            url=f"{API_BASE_URL}/appuser/reglogin",
            params=login_params,
            json=login_payload,
            timeout=10
        )
        login_result = resp.json()
    except Exception as e:
        print(f"[-] 登录请求失败: {e}")
        return None

    if login_result.get("code") == 0:
        token = login_result["data"]["token"]
        print(f"[+] 登录成功，获取到Token")
        return token
    else:
        print(f"[-] 登录失败: {login_result}")
        return None

# 把这里的 bool | None 改成 Optional[bool]
def checkin(token: str) -> Optional[bool]:
    print("\n[步骤2] 正在签到...")
    
    checkin_params = {
        "platform": "web",
        "cur_version": "0.0.0",
        "token": token,
        "deviceinfo": "",
        "lang": "hk",
        "code": "Others"
    }

    try:
        resp = session.post(
            url=f"{API_BASE_URL}/appuser/checkin",
            params=checkin_params,
            json={},
            timeout=10
        )
        checkin_result = resp.json()
    except Exception as e:
        print(f"[-] 签到请求失败: {e}")
        return False

    print(f"[*] 签到返回: {checkin_result}")
    if checkin_result.get("code") == 0:
        print("[+] 签到成功！")
        return True
    return False

if __name__ == "__main__":
    # 调试模式
    # session.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    
    user_token = login()
    if user_token:
        checkin(user_token)
