import requests
import os

pwd=os.path.dirname(os.path.abspath(__file__))
# print(pwd)

img_url = "https://picsum.photos/400/300"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(img_url, headers=headers)

# 自定义文件名（保存在当前目录）
file_name = "/20251228_test_image.png"  # 也可以修改格式为 png/gif 等

if response.status_code == 200:
    with open(pwd+file_name, "wb") as f:
        f.write(response.content)
    print(f"图片已成功保存到当前目录，文件名为：{file_name}")
else:
    print("下载失败")