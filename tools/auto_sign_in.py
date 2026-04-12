import requests
import argparse
import hashlib
from typing import Optional

# ===================== 地址配置 =====================
FRONT_BASE_URL = "http://166.88.141.128:8089"
API_BASE_URL = "https://api.viewturbo.com"
# ===================================================

# 初始化会话
session = requests.Session()
session.headers.update({
    "Host": "api.viewturbo.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Origin": FRONT_BASE_URL,
    "Referer": f"{FRONT_BASE_URL}/",
    "Accept": "application/json",
    "Content-Type": "application/json"
})

def encrypt_password(plain_password: str) -> str:
    """
    将明文密码进行 MD5 加密（与前端加密方式一致）
    """
    return hashlib.md5(plain_password.encode('utf-8')).hexdigest()

def login(email: str, plain_password: str) -> Optional[str]:
    """
    登录获取Token
    :param email: 邮箱账号
    :param plain_password: 明文密码（脚本内部自动MD5加密）
    :return: token字符串或None
    """
    print(f"[步骤1] 正在登录{email}...")

    # 内部进行 MD5 加密
    encrypted_password = encrypt_password(plain_password)

    login_payload = {
        "email": email,
        "password": encrypted_password
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

def checkin(token: str) -> Optional[bool]:
    """
    执行签到
    :param token: 登录后获取的token
    :return: 是否签到成功
    """
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
    parser = argparse.ArgumentParser(description="自动签到脚本 - 输入邮箱和明文密码，自动MD5加密")
    parser.add_argument("--email", "-e", required=True, help="登录邮箱账号")
    parser.add_argument("--password", "-p", required=True, help="明文密码（如 Yy1306332003）")
    args = parser.parse_args()

    # 可选：开启调试代理
    # session.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

    user_token = login(args.email, args.password)
    if user_token:
        checkin(user_token)