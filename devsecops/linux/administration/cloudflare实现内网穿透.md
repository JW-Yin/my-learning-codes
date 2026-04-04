# 【Fedora + Cloudflare 隧道 极速部署手册】
**极简无坑版**（避开所有权限/Token/冲突报错，直接复制运行）
适用：任意 Fedora 机器，无公网IP、家用内网/手机热点均可

---

## 一、前置条件（一次准备）
1. Cloudflare 账号：https://dash.cloudflare.com/
2. 域名已托管到 Cloudflare（DNS 服务器改为 CF 提供的）
3. 本地服务端口：如 `8080`

---

## 二、单机器极速部署（全程复制命令）
### 1. 安装 cloudflared
```bash
wget -O cloudflared.rpm https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm
sudo dnf install -y ./cloudflared.rpm
cloudflared --version
```

### 2. 登录 Cloudflare（绑定域名）
```bash
cloudflared tunnel login
```
→ 打开链接授权，选择你的域名

### 3. 创建隧道（名字自定义，如 `fedora-server`）
```bash
cloudflared tunnel create fedora-server
```
→ 记录**隧道ID**（备用，这里直接用名字即可）

### 4. 绑定域名到隧道（替换为你的子域名）
```bash
cloudflared tunnel route dns fedora-server fedora.你的域名
```

### 5. 【关键】后台永久运行（无冲突、无闪退）
**不创建 config.yml、不用 root 服务**，纯普通用户运行：
```bash
nohup cloudflared tunnel run --url http://localhost:8080 fedora-server > ~/cf.log 2>&1 &
```

### 6. 开机自启（重启自动跑）
```bash
echo "@reboot nohup cloudflared tunnel run --url http://localhost:8080 fedora-server > ~/cf.log 2>&1 &" | crontab -
```

---

## 三、验证是否成功
```bash
# 查看进程
ps aux | grep cloudflared
# 查看日志
tail -f ~/cf.log
```
→ 出现 `Registered tunnel connection` = 成功
→ 公网访问：`https://fedora.你的域名.xyz`

---

## 四、绝对避坑规则（核心！）
1. **不手动创建 `config.yml`** → 与 `--url` 冲突必闪退
2. **不用 `sudo cloudflared service install`** → 必报 Token 无效
3. **全程普通用户运行** → 避开 root 权限问题
4. 只用 `nohup + crontab @reboot` → 最稳定、零报错

---

## 五、常用管理命令
```bash
# 停止隧道
pkill -f cloudflared

# 重启隧道
nohup cloudflared tunnel run --url http://localhost:8080 fedora-server > ~/cf.log 2>&1 &

# 查看实时日志
tail -f ~/cf.log
```

---

# 最终效果
✅ 无公网IP / 无端口映射 / 无防火墙开放
✅ 免费 HTTPS
✅ 后台常驻 + 开机自启
✅ 公网域名直接访问本地服务
---
```bash
# 1. 安装
wget -O cloudflared.rpm https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm
sudo dnf install -y ./cloudflared.rpm

# 2. 登录+创建隧道+绑定域名
cloudflared tunnel login
cloudflared tunnel create fedora-server
cloudflared tunnel route dns fedora-server fedora.jw-yin.xyz

# 3. 后台永久运行
nohup cloudflared tunnel run --url http://localhost:8080 fedora-server > ~/cf.log 2>&1 &

# 4. 开机自启
echo "@reboot nohup cloudflared tunnel run --url http://localhost:8080 fedora-server > ~/cf.log 2>&1 &" | crontab -

```