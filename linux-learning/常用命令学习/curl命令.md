# curl 命令完整学习指南
## 一、背景与定位
在无图形界面的 Linux 环境中，**测试 API、自定义 HTTP 请求、灵活下载/上传文件**是高频需求，传统工具（如 wget）功能单一，无法满足复杂场景。curl 就是为解决这个问题而生的**全能型多协议网络请求工具**。

- **全称**：Client URL（客户端 URL 工具）
- **核心优势**：支持 HTTP/HTTPS/FTP/SFTP 等数十种协议，可完全自定义请求头、请求体、Cookie、代理等，是 API 调试、网络交互的首选工具。

---

## 二、前置准备：安装与验证
你使用的 Ubuntu 22.04 通常默认自带 curl，缺失时执行：
```bash
sudo apt update && sudo apt install curl
```
验证安装：
```bash
curl -V  # 注意是大写 V，查看版本
```

---

## 三、基础语法
```bash
curl [全局选项] [URL]
```
核心规则：
- `-` 开头为**短参数**（如 `-o`），`--` 开头为**长参数**（如 `--output`）
- 所有参数均标注**英文全称**，方便理解记忆

---

## 四、高频核心参数与实战
### （一）文件下载类（基础但常用）
| 参数 | 英文全称 | 用途 | 示例 |
|------|----------|------|------|
| `-o` | `--output` | 指定保存的**文件名/路径**（必须写文件名） | `curl -o /home/ubuntu/baidu.html https://www.baidu.com` |
| `-O` | `--remote-name` | 自动使用 URL 中的**原文件名**保存（无需写文件名） | `curl -O https://mirrors.aliyun.com/ubuntu-releases/22.04.3/ubuntu-22.04.3-desktop-amd64.iso` |
| `-C -` | `--continue-at -` | **断点续传**（`-` 表示自动从断点继续） | `curl -C - -O https://mirrors.aliyun.com/ubuntu-releases/22.04.3/ubuntu-22.04.3-desktop-amd64.iso` |
| `--limit-rate` | `--limit-rate` | **限速下载**（单位：`k`=KB/s，`m`=MB/s） | `curl --limit-rate 100k -O https://mirrors.aliyun.com/ubuntu-releases/22.04.3/ubuntu-22.04.3-desktop-amd64.iso` |
| `-L` | `--location` | **跟随重定向**（301/302 自动跳转，下载必加） | `curl -L -O https://baidu.com/file.zip` |
| `-k` | `--insecure` | **忽略 HTTPS 证书错误**（用于自签名证书） | `curl -k -O https://self-signed.example.com/file.zip` |

---

### （二）API 测试与 HTTP 请求类（curl 核心优势）
| 参数 | 英文全称 | 用途 | 示例 |
|------|----------|------|------|
| `-I` | `--head` | 只获取 **HTTP 响应头**（不下载内容，快速检查接口状态） | `curl -I https://www.baidu.com` |
| `-X` | `--request` | 指定 **HTTP 请求方法**（GET/POST/PUT/DELETE 等） | `curl -X POST https://example.com/api` |
| `-H` | `--header` | 添加 **自定义请求头**（可多次使用） | `curl -H "Content-Type: application/json" -H "Authorization: Bearer token123" https://example.com/api` |
| `-d` | `--data` | 发送 **POST 请求数据**（表单/JSON 等） | 表单：`curl -X POST -d "username=test&password=123" https://example.com/login`<br>JSON：`curl -X POST -H "Content-Type: application/json" -d '{"name":"test","age":20}' https://example.com/api` |
| `-G` | `--get` | 将 `-d` 的数据作为 **GET 请求参数**（自动拼接到 URL） | `curl -G -d "key=1&name=2" https://example.com/api` |
| `-u` | `--user` | 发送 **HTTP 基本认证**（用户名:密码） | `curl -u admin:123456 https://example.com/protected` |

---

### （三）输出与调试类（定位问题必备）
| 参数 | 英文全称 | 用途 | 示例 |
|------|----------|------|------|
| `-v` | `--verbose` | 显示**详细请求/响应过程**（调试核心，能看到握手、请求头、响应头） | `curl -v https://www.baidu.com` |
| `-s` | `--silent` | **静默模式**（不输出进度条和错误） | `curl -s https://www.baidu.com` |
| `-S` | `--show-error` | 配合 `-s` 使用，**只显示错误**（静默但报错） | `curl -sS https://www.baidu.com` |
| `-w` | `--write-out` | 自定义输出**请求元数据**（如 HTTP 状态码、耗时） | `curl -w "HTTP状态码: %{http_code}\n总耗时: %{time_total}s\n" -o /dev/null -s https://www.baidu.com` |
| `-o /dev/null` | `--output /dev/null` | 不保存内容，只看输出（配合 `-w` 使用） | 同上 |

---

### （四）高级功能类（复杂场景必备）
| 参数 | 英文全称 | 用途 | 示例 |
|------|----------|------|------|
| `-A` | `--user-agent` | 自定义 **User-Agent**（模拟浏览器，绕过反爬） | `curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" https://www.baidu.com` |
| `-b` | `--cookie` | 发送 **Cookie**（字符串或文件） | 字符串：`curl -b "sessionid=abc123; username=test" https://example.com`<br>文件：`curl -b cookies.txt https://example.com` |
| `-c` | `--cookie-jar` | 保存 **Cookie 到文件**（登录后保存会话） | `curl -c cookies.txt https://example.com/login` |
| `-T` | `--upload-file` | **上传文件**（FTP/SFTP 等） | `curl -T /home/ubuntu/test.zip ftp://ftp.example.com/upload/` |
| `-x` | `--proxy` | 使用 **HTTP/HTTPS 代理** | `curl -x http://127.0.0.1:7890 https://www.google.com`（仅示例，大陆无法访问） |

---

## 五、避坑指南（高频错误）
1. **`-o` vs `-O` 区别**：`-o` 必须写文件名（如 `curl -o test.html https://example.com`），`-O` 自动用原文件名（如 `curl -O https://example.com/test.html`），不要搞混。
2. **GET 请求带参数**：URL 必须加**双引号**，避免 `&` 被 shell 解析为后台命令（如 `curl "https://example.com/api?key=1&name=2"`）。
3. **POST JSON 数据**：必须加 `-H "Content-Type: application/json"`，否则服务器无法解析。
4. **跟随重定向**：下载或访问跳转链接时，必须加 `-L`，否则只会返回 301/302 响应头，不会跳转。
5. **`-C -` 的短横线**：断点续传的 `-C -` 中，第二个短横线不能少，否则需要手动指定断点位置。

---

## 六、学习路径建议
1. **入门**：先练熟 `curl -o`/`-O`/`-L` 下载文件、`curl -I` 检查接口状态。
2. **进阶**：掌握 `curl -X`/`-H`/`-d` 测试 API、`curl -v` 调试请求。
3. **精通**：灵活组合参数（如带 Cookie/代理上传文件、用 `-w` 监控接口性能）。
