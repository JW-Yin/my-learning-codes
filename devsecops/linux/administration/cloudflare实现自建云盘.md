我给你整理**终极极简速查版**！
**任何新的 Linux/Fedora 设备**，直接按这个顺序复制粘贴，**1 分钟部署好公网网盘**，完全复刻你现在稳定的状态，零报错、无坑！

---

# 🚀 新设备 一键部署公网网盘（最终版）
## 【第一步】安装并配置 Cloudflare 隧道（8080 端口）
```bash
# 1. 安装 cloudflared
wget -O cloudflared.rpm https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm
sudo dnf install -y ./cloudflared.rpm

# 2. 登录 Cloudflare + 创建隧道 + 绑定域名
cloudflared tunnel login
cloudflared tunnel create fedora-server
cloudflared tunnel route dns fedora-server fedora.jw-yin.xyz

# 3. 后台启动隧道 + 开机自启
nohup cloudflared tunnel run --url http://localhost:8080 fedora-server > ~/cf.log 2>&1 &
echo "@reboot nohup cloudflared tunnel run --url http://localhost:8080 fedora-server > ~/cf.log 2>&1 &" | crontab -
```

---

## 【第二步】安装 FileBrowser 网盘（手动安装，永不失败）
```bash
# 1. 下载安装包（国内可下载）
cd ~/下载
wget https://github.com/filebrowser/filebrowser/releases/latest/download/linux-amd64-filebrowser.tar.gz

# 2. 解压+安装到系统
tar -zxvf linux-amd64-filebrowser.tar.gz
sudo mv filebrowser /usr/local/bin/
sudo chmod +x /usr/local/bin/filebrowser
```

---

## 【第三步】启动网盘（公网直接访问）
```bash
# 1. 首次启动（看日志获取随机密码！）
filebrowser -a 0.0.0.0 -p 8080 -r ~/公共 -d ~/.filebrowser.db
```

### ✔ 关键看终端日志！会出现这一行：
```
User 'admin' initialized with randomly generated password: 【你的随机密码】
```

---

## 【第四步】登录后，后台永久运行
```bash
# 按 Ctrl+C 停止前台进程
# 后台启动（关闭终端不退出）
nohup filebrowser -a 0.0.0.0 -p 8080 -r ~/公共 -d ~/.filebrowser.db > ~/fb.log 2>&1 &
```

---

# 🌐 公网访问地址（所有设备通用）
```
https://fedora.jw-yin.xyz
```

---

# 📌 3 个必记关键点（防踩坑）
1. **用户名永远是 `admin`**
2. **密码不是 admin！是首次启动时终端里的随机密码**
3. **全程只占用 8080 端口，最稳定、无 1033、无冲突**

---

# ✅ 完成！
新设备现在 = **公网可访问的私人网盘**
任何手机/电脑/平板，打开浏览器就能用！