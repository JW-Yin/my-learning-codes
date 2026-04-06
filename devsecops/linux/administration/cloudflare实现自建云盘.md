# 🚀 Fedora 一键部署：Docker FileBrowser + Cloudflare 隧道（终极速查版）
**适用于任何新 Fedora 系统，全程复制粘贴，100%复刻当前稳定状态**

## 一、前置：彻底清理裸机残留（新系统可跳过）
```bash
# 杀死进程
pkill -f filebrowser cloudflared
# 删除文件
sudo rm -f /usr/local/bin/filebrowser
rm -f ~/.filebrowser.db ~/fb.log ~/cf.log
rm -rf ~/.cloudflared
# 卸载cloudflared
sudo dnf remove -y cloudflared
# 清空crontab
crontab -r
```

## 二、Docker 部署 FileBrowser（核心，监听8080）
```bash
# 启动容器（端口8080，挂载~/公共，开机自启）
docker run -d \
  --name filebrowser \
  --restart always \
  -p 8080:80 \
  -v ~/公共:/srv \
  -v filebrowser_data:/database \
  filebrowser/filebrowser:v2-s6

# 查看初始密码
docker logs filebrowser | grep "password"
```
> 账号：`admin` | 密码：日志中随机字符串

## 三、安装 & 配置 Cloudflare 隧道（Fedora专属）
```bash
# 1. 安装cloudflared
wget -O cloudflared.rpm https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm
sudo dnf install -y ./cloudflared.rpm

# 2. 登录Cloudflare（浏览器授权，自动生成证书）
cloudflared tunnel login

# 3. 前台启动隧道（输密码，看到Connection established即成功）
sudo cloudflared tunnel run --url http://127.0.0.1:8080 fedora-server
# 按Ctrl+Z暂停 → 丢后台运行
bg
disown
```

## 四、配置开机自启（永久生效）
```bash
# crontab添加sudo自启
echo "@reboot sudo cloudflared tunnel run --url http://127.0.0.1:8080 fedora-server > ~/cf.log 2>&1" | crontab -
```

## 五、验证 & 访问
```bash
# 查看隧道状态
cat ~/cf.log
# 公网访问（你的域名）
https://fedora.jw-yin.xyz
```

---

# ✅ 核心关键点（必记）
1. FileBrowser 固定 **8080端口**（`-p 8080:80`），隧道直接对接
2. cloudflared 必须 **sudo 运行**（解决凭证权限问题）
3. 全程 Docker 化 FileBrowser，裸机仅留隧道，干净稳定
4. 开机自启通过 crontab + sudo，重启自动运行