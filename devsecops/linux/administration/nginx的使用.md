# Nginx 完整复盘清单（静态部署+核心扩展）
## 适用场景：Linux（Ubuntu/Debian）系统下 Nginx 部署与配置
核心逻辑：「安装 → 基础配置 → 业务部署 → 验证 → 扩展（反向代理/负载均衡）」

---

## 一、基础部署：静态 HTML 页面（核心流程）
### 1. 环境准备（可选但推荐）
```bash
sudo apt update  # 更新软件源，避免安装包版本过旧
```

### 2. 安装 Nginx
```bash
sudo apt install nginx -y  # -y 自动确认安装，无需手动交互
```
- 安装后自动创建关键目录：
  - 静态资源根目录：`/var/www/html`（存放 HTML/CSS/JS 等）
  - 配置文件主目录：`/etc/nginx`（核心配置、站点配置）
  - 日志目录：`/var/log/nginx`（access.log 访问日志、error.log 错误日志）

### 3. 启动与开机自启（关键）
```bash
sudo systemctl start nginx        # 启动 Nginx
sudo systemctl enable nginx       # 设置开机自启（服务器重启后自动运行）
sudo systemctl status nginx       # 验证运行状态（正常显示 active (running)）
```

### 4. 端口放行（必做，外部访问核心）
Nginx 默认监听 80 端口，需同时放行「服务器本地防火墙 + 云服务商安全组」：
#### （1）服务器本地防火墙（Ubuntu/Debian）
```bash
sudo ufw status                  # 查看防火墙状态
sudo ufw allow 80/tcp && sudo ufw reload  # 放行80端口并重载规则
```
#### （2）云服务商安全组（阿里云/腾讯云等）
登录控制台 → 安全组 → 入站规则 → 添加：
- 协议：TCP
- 端口：80
- 授权对象：0.0.0.0/0（允许所有IP访问）

### 5. 部署静态 HTML 文件
#### 方式 1：创建测试文件（快速验证）
```bash
sudo vim /var/www/html/index.html  # Nginx 优先加载 index.html
```
粘贴测试内容：
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Nginx 测试页面</title>
</head>
<body>
    <h1 style="color: #2ecc71;">Nginx 部署成功！</h1>
    <p>访问路径：http://你的服务器公网IP</p>
</body>
</html>
```
#### 方式 2：上传本地 HTML 文件
```bash
# 本地终端执行，将本地文件传到服务器静态目录
scp /本地文件路径/xxx.html 服务器用户名@服务器IP:/var/www/html/
# 示例：scp ~/Desktop/mypage.html jw-yin@123.57.139.216:/var/www/html/
```

### 6. 权限配置（避免 403 错误，推荐）
Nginx 工作进程以 `www-data` 用户运行，需确保文件可被读取：
```bash
sudo chmod -R 755 /var/www/html/          # 递归设置目录权限（可读可执行）
sudo chown -R www-data:www-data /var/www/html/  # 递归设置文件归属
```

### 7. 验证部署结果
#### （1）服务器内自测（快速确认）
```bash
curl http://127.0.0.1  # 输出 HTML 内容 → 本地访问正常
```
#### （2）外部浏览器验证（最终确认）
输入 `http://你的服务器公网IP`：
- 显示测试页面 → 部署成功；
- 超时/打不开 → 检查 80 端口放行；
- 403 Forbidden → 检查文件权限。

---

## 二、核心扩展：反向代理/负载均衡（Nginx 核心能力）
### 1. 配置文件结构（重点）
- 主配置文件：`/etc/nginx/nginx.conf`（仅管全局规则，如用户、进程数，默认无需改）；
- 站点配置目录：`/etc/nginx/sites-available/`（改这里！存放所有站点/服务配置）；
- 启用站点目录：`/etc/nginx/sites-enabled/`（软链接指向 `sites-available/` 的配置文件）。

### 2. 反向代理配置（单后端）
编辑默认站点配置：
```bash
sudo vim /etc/nginx/sites-available/default
```
在 `server` 块中添加反向代理规则：
```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8080/;  # 转发到本地8080端口的后端服务
    proxy_set_header Host $host;        # 传递请求头（必加，避免后端识别异常）
    proxy_set_header X-Real-IP $remote_addr;  # 传递真实客户端IP
}
```

### 3. 负载均衡配置（多后端）
同样编辑 `sites-available/default`，先定义「后端服务器池」，再转发：
```nginx
# 1. 在 http 块内、server 块外定义后端池（命名为 backend_pool）
upstream backend_pool {
    server 127.0.0.1:8080;  # 后端服务1
    server 127.0.0.1:8081;  # 后端服务2
    # 可选规则：weight=数值（权重）、ip_hash（会话保持）
}

# 2. 在 server 块内添加转发规则
server {
    listen 80 default_server;
    root /var/www/html;
    index index.html;

    location /api/ {
        proxy_pass http://backend_pool/;  # 转发到后端池
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. 配置生效（必做步骤）
```bash
sudo nginx -t  # 验证配置语法（核心！避免改错导致Nginx启动失败）
sudo systemctl restart nginx  # 重启Nginx使配置生效
```

---

## 三、常用运维命令（复盘/排错必备）
| 场景                  | 命令                                  | 作用说明                     |
|-----------------------|---------------------------------------|------------------------------|
| 重启 Nginx（配置生效） | sudo systemctl restart nginx          | 加载新配置                   |
| 停止 Nginx            | sudo systemctl stop nginx             | 停止服务                     |
| 查看运行状态          | sudo systemctl status nginx           | 确认是否 active (running)    |
| 查看80端口监听        | ss -tulpn \| grep 80                  | 确认Nginx是否监听80端口      |
| 验证配置语法          | sudo nginx -t                         | 检查配置文件是否有语法错误   |
| 查看访问日志（排错）  | tail -f /var/log/nginx/access.log     | 实时查看用户访问记录         |
| 查看错误日志（排错）  | tail -f /var/log/nginx/error.log      | 实时查看报错信息             |
| 启用新站点            | sudo ln -s /etc/nginx/sites-available/xxx.conf /etc/nginx/sites-enabled/ | 软链接启用配置 |
| 禁用站点              | sudo rm /etc/nginx/sites-enabled/xxx.conf | 仅删软链接，保留原配置       |

---

## 四、核心关键点回顾（复盘核心）
1. **核心目录**：`/var/www/html` 是静态资源默认根目录，优先加载 `index.html`；`/etc/nginx/sites-available/` 是配置主战场，99%的玩法都改这里。
2. **端口放行**：80端口需同时放行「服务器防火墙 + 云安全组」，缺一不可。
3. **权限问题**：403错误大概率是文件归属/权限问题，执行 `chmod 755` + `chown www-data` 可解决。
4. **配置验证**：改完配置必先执行 `nginx -t` 验证语法，再重启，避免Nginx宕机。
5. **进程架构**：Nginx主进程(root)负责监听端口，工作进程(www-data)处理请求，是安全的最小权限设计。
6. **核心能力**：静态部署是基础，反向代理是核心（隐藏后端细节），负载均衡是反向代理的进阶（多后端分发）。



# 一、最常见 4xx（客户端错误）
## 400 Bad Request
- 含义：**请求语法错了**
- 场景：URL 乱填、参数格式不对、请求头乱了
- 人话：服务器看不懂你发的是啥

## 401 Unauthorized
- 含义：**未登录 / 没身份**
- 场景：需要登录但你没登
- 人话：你谁啊？先登录再来

## 403 Forbidden
- 含义：**服务器理解你，但拒绝访问**
- 场景：
  - 文件权限不对（Nginx 最常见）
  - 目录没有默认 index.html
  - 权限不足、被防火墙策略拒绝
- 人话：我知道你是谁，但我就是不给你看

## 404 Not Found
- 含义：**资源不存在**
- 场景：URL 写错、文件删了、路径不对
- 人话：你要的东西我这儿没有

---

# 二、最常见 5xx（服务器错误）
## 500 Internal Server Error
- 含义：**服务器代码/配置炸了**
- 场景：Nginx 配置写错、后端代码崩溃
- 人话：服务器自己出 bug 了

## 502 Bad Gateway
- 含义：**网关收到了无效响应**
- 场景：Nginx 反向代理，但后端没启动/挂了
- 人话：我帮你转发了，但后端不理我

## 503 Service Unavailable
- 含义：**服务暂时不可用**
- 场景：维护、超载、限流
- 人话：我现在忙不过来，等会儿再来

## 504 Gateway Timeout
- 含义：**网关超时，后端没响应**
- 场景：后端服务卡死、太慢
- 人话：我等了半天，后端不回我

---

# 三、最常见 2xx / 3xx（成功/重定向）
## 200 OK
- 成功，一切正常

## 301 Moved Permanently
- 永久跳转（旧网址废弃）

## 302 Found / 307 Temporary Redirect
- 临时跳转
- 场景：HTTP 自动跳 HTTPS

---

# 五、超级精简记忆版（背这个）
- **200** 正常
- **301/302** 跳转
- **400** 请求格式错
- **401** 没登录
- **403** 权限问题
- **404** 找不到页面
- **500** 服务器炸
- **502** 后端没启动/挂了
- **504** 后端超时
