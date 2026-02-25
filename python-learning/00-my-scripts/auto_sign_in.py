import requests
import time  # 新增：导入时间模块
from requests.exceptions import RequestException, JSONDecodeError

def send_analytics_post():
    """封装 POST 请求，动态生成毫秒级时间戳"""
    url = "https://analytics.editcookie.com/submit"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "chrome-extension://hihblcmlaaademjlakdpicchbjnnnkbo",
        "Accept": "*/*",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Storage-Access": "active",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh,zh-CN;q=0.9",
        "Priority": "u=1, i"
    }

    # 动态生成毫秒级时间戳
    current_timestamp = int(time.time() * 1000)
    print(f"本次请求使用的时间戳：{current_timestamp}")

    # 请求体（动态 timestamp）
    payload = {
        "name": "SO",
        "data": [
            {
                "url": "http://166.88.141.128:8089/zh/my/?platform=linux&cur_version=1.12.0&deviceinfo=Ubuntu&code=Others",
                "timestamp": current_timestamp,  # 动态值
                "user_id": "b9f5ccc3a5fe4e01848add03a3a9e377"
            }
        ]
    }

    try:
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=10,  # 10秒超时
            verify=False
        )
        response.raise_for_status()  # 抛出HTTP错误

        # 解析响应
        try:
            result = response.json()
            print("请求成功，响应JSON：", result)
            return result
        except JSONDecodeError:
            print("请求成功，响应非JSON：", response.text)
            return response.text

    except RequestException as e:
        print(f"请求失败：{e}")
        return None

# 调用函数
if __name__ == "__main__":
    send_analytics_post()
