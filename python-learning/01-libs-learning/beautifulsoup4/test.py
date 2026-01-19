import requests
from bs4 import BeautifulSoup

url = "https://baidu.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 发送GET请求，获取响应文本（HTML）
response = requests.get(url=url, headers=headers, timeout=15)
response.raise_for_status()  # 确保请求成功
html_content = response.text

# 1. 初始化BeautifulSoup解析对象（核心：把HTML文本变成可操作的“标签树”）
# 第一个参数：要解析的HTML内容
# 第二个参数：解析器（html.parser 是Python内置的，无需额外安装，适合小白）
soup = BeautifulSoup(html_content, "html.parser")

# 打印提示，说明初始化成功
print("✅ HTML获取成功并完成解析，接下来可以提取表单了")

# 2. 提取单个form标签（使用find()方法，找第一个匹配的<form>标签）
# 括号内传入标签名"form"，表示要查找<form>标签
single_form = soup.find("form")

# 先判断是否找到form标签（避免找不到导致后续报错，小白必学的空值处理）
if single_form:
    print("\n===== 提取单个form标签的属性 =====")
    # 3. 提取form标签的属性（使用attrs.get()方法，安全获取属性，避免属性不存在报错）
    # 提取action属性（表单提交地址）
    form_action = single_form.attrs.get("action", "无该属性")  # 第二个参数是默认值，属性不存在时返回
    # 提取method属性（表单提交方式）
    form_method = single_form.attrs.get("method", "无该属性").upper()  # 转大写，统一格式
    
    # 打印结果
    print(f"form标签的action（提交地址）：{form_action}")
    print(f"form标签的method（提交方式）：{form_method}")
else:
    print("\n❌ 未找到任何form标签")


# 7. 提取form标签内的所有表单字段（在已找到的single_form内查找，而非整个soup）
if single_form:
    print("\n===== 提取form内的所有表单字段 =====")
    # 7.1 提取所有<input>标签（使用find_all()方法，查找所有匹配的标签，返回列表）
    input_list = single_form.find_all("input")  # 只在single_form这个form标签内查找，避免获取其他form的字段
    
    # 7.2 遍历所有<input>标签，提取关键信息
    for index, input_tag in enumerate(input_list, 1):  # enumerate：带索引遍历，方便计数
        print(f"\n--- 字段{index} ---")
        # 提取<input>的核心属性
        input_type = input_tag.attrs.get("type", "无该属性")  # 字段类型（text/ password/ button等）
        input_name = input_tag.attrs.get("name", "无该属性")  # 字段名称（后台接收数据的标识）
        input_value = input_tag.attrs.get("value", "无该属性")  # 字段默认值
        input_placeholder = input_tag.attrs.get("placeholder", "无该属性")  # 输入框提示文字
        
        # 打印字段信息
        print(f"  类型（type）：{input_type}")
        print(f"  名称（name）：{input_name}")
        print(f"  默认值（value）：{input_value}")
        print(f"  提示文字（placeholder）：{input_placeholder}")
    
    # 7.3 拓展：提取<textarea>（多行输入框，比如留言框）
    textarea_tag = single_form.find("textarea")
    if textarea_tag:
        print("\n--- 多行输入框（textarea）---")
        textarea_name = textarea_tag.attrs.get("name", "无该属性")
        textarea_placeholder = textarea_tag.attrs.get("placeholder", "无该属性")
        print(f"  名称（name）：{textarea_name}")
        print(f"  提示文字（placeholder）：{textarea_placeholder}")
