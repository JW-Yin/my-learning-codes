from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# 1. 发送请求获取HTML（和原来一样）
url = "http://www.baidu.com"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"}
response = requests.get(url=url, headers=headers, timeout=15)
response.raise_for_status()
html_content = response.text

# 2. 创建BeautifulSoup解析对象
soup = BeautifulSoup(html_content, "lxml")

# 精准定位name="username"的<input>标签（精确匹配）
username_input = soup.select_one('input[name="username"]')  # 注意：属性值引号可单可双

# 3. 提取所有表单的action和method属性
all_forms = soup.select("form[action]") #定位所有带action属性的<form>标签（项目中过滤无效表单）
for idx, form in enumerate(all_forms, 1):
    print(f"=== 第{idx}个表单信息 ===")
    # 提取action属性（推荐get()方法，容错高）
    form_action = form.get("action")
    # 提取method属性，若缺失则默认返回"GET"（表单默认提交方式）
    form_method = form.get("method", "GET").upper()  # upper()转为大写，格式统一
    print(f"提交接口（action）：{form_action}")
    # 用urljoin()转换相对URL为绝对URL
    print(f"提交接口的绝对路径为（action）：{urljoin(url, form_action)}")
    print(f"提交方式（method）：{form_method}")
    
    
    # 4. 提取该表单内所有<input>的name和type属性
    all_inputs = form.select("input[name]") #定位所有带name属性的<input>标签
    print(f"该表单输入字段总数：{len(all_inputs)}")
    for input_tag in all_inputs:
        input_name = input_tag.get("name")
        input_type = input_tag.get("type", "text")  # 若缺失type，默认是text
        print(f"  - 字段名（name）= {input_name}，字段类型（type）= {input_type}")
    print("-" * 50)