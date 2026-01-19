from urllib.parse import urljoin

# 场景1：基础URL结尾无斜杠
base1 = "https://网站.com/page"
print(urljoin(base1, "image/logo.png"))  
# 输出：https://网站.com/image/logo.png（自动补全路径层级）

# 场景2：相对URL是根路径开头
base2 = "https://网站.com/a/b/c"
print(urljoin(base2, "/image/logo.png")) 
# 输出：https://网站.com/image/logo.png（识别根路径）

# 场景3：相对URL包含层级跳转
base3 = "https://网站.com/a/b/c"
print(urljoin(base3, "../image/logo.png")) 
# 输出：https://网站.com/a/b/image/logo.png（自动回退一级目录）
