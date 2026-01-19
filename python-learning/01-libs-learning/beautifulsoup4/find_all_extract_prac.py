import requests
from bs4 import BeautifulSoup

def extract_all_forms(target_url: str):
    """
    提取目标网页的所有form标签及内部表单字段
    :param target_url: 目标网页URL
    """
    # 1. 配置请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 2. 发送请求获取HTML
        response = requests.get(target_url, headers=headers, timeout=15)
        response.raise_for_status()
        html_content = response.text

        # 3. 初始化BeautifulSoup解析对象
        soup = BeautifulSoup(html_content, "html.parser")

        # 4. 提取所有form标签（使用find_all()，返回列表）
        all_forms = soup.find_all("form")

        if not all_forms:
            print("❌ 未找到任何form标签")
            return

        print(f"✅ 成功找到 {len(all_forms)} 个form标签，开始逐个解析\n")

        # 5. 遍历所有form标签，逐个解析
        for form_index, form_tag in enumerate(all_forms, 1):
            print(f"===== 第 {form_index} 个form标签 =====")
            # 5.1 提取form标签自身属性
            form_action = form_tag.attrs.get("action", "无该属性")
            form_method = form_tag.attrs.get("method", "无该属性").upper()
            print(f"1. form属性：")
            print(f"   - 提交地址（action）：{form_action}")
            print(f"   - 提交方式（method）：{form_method}")

            # 5.2 提取form内的所有表单字段
            print(f"2. 表单字段：")
            # 提取所有<input>标签
            input_tags = form_tag.find_all("input")
            # 提取所有<textarea>标签
            textarea_tags = form_tag.find_all("textarea")
            # 提取所有<select>标签（下拉选择框）
            select_tags = form_tag.find_all("select")

            # 合并所有字段（便于统一遍历）
            all_fields = []
            for input_tag in input_tags:
                all_fields.append(("input", input_tag))
            for textarea_tag in textarea_tags:
                all_fields.append(("textarea", textarea_tag))
            for select_tag in select_tags:
                all_fields.append(("select", select_tag))

            # 遍历并打印所有字段
            if not all_fields:
                print("   - 无任何表单字段")
                continue

            for field_index, (field_type, field_tag) in enumerate(all_fields, 1):
                print(f"   - 字段{field_index}（类型：{field_type}）：")
                # 提取通用属性
                field_name = field_tag.attrs.get("name", "无该属性")
                field_value = field_tag.attrs.get("value", "无该属性")
                print(f"      名称：{field_name}")
                print(f"      默认值：{field_value}")

                # 针对不同字段类型，提取特有属性
                if field_type == "input":
                    field_input_type = field_tag.attrs.get("type", "无该属性")
                    field_placeholder = field_tag.attrs.get("placeholder", "无该属性")
                    print(f"      输入类型：{field_input_type}")
                    print(f"      提示文字：{field_placeholder}")
                elif field_type == "textarea":
                    field_rows = field_tag.attrs.get("rows", "无该属性")
                    field_cols = field_tag.attrs.get("cols", "无该属性")
                    print(f"      行数：{field_rows}")
                    print(f"      列数：{field_cols}")

            print("\n" + "-" * 50 + "\n")

    except Exception as e:
        print(f"❌ 程序出错：{str(e)}")

if __name__ == "__main__":
    TARGET_URL = "https://baidu.com"  # 百度登录页（带表单，适合测试）
    extract_all_forms(TARGET_URL)