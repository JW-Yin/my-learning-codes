from urllib.parse import urlparse

# 目标域名（原网页URL，项目中存放于config.py）
target_url = "https://example.com/page1.html"

# 解析目标URL，获取域名
parsed_target = urlparse(target_url)
target_domain = parsed_target.netloc  # 提取域名（核心属性）
print(f"目标域名：{target_domain}")

# 待筛选的绝对URL列表
absolute_urls = [
    "https://example.com/about",
    "https://example.com/contact",
    "https://google.com",
    "https://www.example.com/news"  # 注意：www.example.com 和 example.com 视为不同域名
    # 筛选前要统一域名格式（要么都去掉www.，要么都加上www.）（可通过正则表达式实现）
]

# 筛选同域名链接
same_domain_urls = []
for url in absolute_urls:
    parsed_url = urlparse(url)
    current_domain = parsed_url.netloc
    if current_domain == target_domain:
        same_domain_urls.append(url)

print(f"\n同域名链接列表：\n{same_domain_urls}")