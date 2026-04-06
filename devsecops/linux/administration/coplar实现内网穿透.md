
# Fedora 快速部署 Cpolar (8080端口)
## 前置准备
1. 去 [cpolar官网](https://dashboard.cpolar.com/get-started) 注册账号，复制你的 **Authtoken**
2. 确保本地 8080 端口有服务在运行

---

## 1. 安装 Cpolar
(官网下载.zip文件)`https://dashboard.cpolar.com/get-started`

```bash
# 解压
unzip cpolar-stable-linux-amd64.zip

# 移动到系统目录并授权
sudo mv cpolar /usr/local/bin/
sudo chmod +x /usr/local/bin/cpolar
```

---

## 2. 绑定 Authtoken
```bash
# 替换为你自己的 Authtoken
cpolar authtoken 你的Authtoken
```

---

## 3. 编写配置文件 (8080端口)
```bash
vim ~/.cpolar/cpolar.yml
```
**完整内容如下**（直接复制，替换 Authtoken）：
```yaml
authtoken: 你的Authtoken
region: cn
tunnels:
  web:
    proto: http
    addr: 8080
```

---

## 4. 设置开机自启 (Systemd)
```bash
sudo vim /etc/systemd/system/cpolar.service
```
**完整内容如下**（直接复制）：
```ini
[Unit]
Description=Cpolar
After=network.target

[Service]
User=你的用户名
ExecStart=/usr/local/bin/cpolar start-all
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
⚠️ **注意**：把 `User=你的用户名` 改成你 Fedora 的实际用户名（比如 `jw-yin`）

---

## 5. 修复 SELinux (Fedora 特有关键步骤)
```bash
# 修复文件安全标签
sudo chcon -t bin_t /usr/local/bin/cpolar

# 生成并安装 SELinux 策略模块
sudo ausearch -m avc -ts recent | audit2allow -M cpolar
sudo semodule -i cpolar.pp
```

---

## 6. 启动服务并验证
```bash
# 重载并启动
sudo systemctl daemon-reload
sudo systemctl enable cpolar
sudo systemctl start cpolar

# 查看日志确认隧道建立（找 Forwarding 那一行）
sudo journalctl -u cpolar -n 20 --no-pager
```

---

## 7. 公网访问
在日志里找到类似这一行：
```
Forwarding  https://xxxx.cpolar.io -> localhost:8080
```
直接用浏览器访问那个 `https` 地址即可！

---

## 常用管理命令
```bash
# 查看服务状态
sudo systemctl status cpolar

# 重启服务
sudo systemctl restart cpolar

# 查看实时日志
sudo journalctl -u cpolar -f

# 启动 Web 管理面板 (访问 http://127.0.0.1:4040)
cpolar web ui &
```

---

### 总结
这份指南**跳过了所有调试过程**，直接给出最稳定的配置，在另一台 Fedora 上按顺序执行，**5 分钟内就能完成 8080 端口的内网穿透并开机自启**。