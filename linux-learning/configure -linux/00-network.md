
### 先更换ubuntu的下载源

---

### 第一步：先确认你的无线网卡型号（精准定位问题）
打开终端执行：
```bash
lspci | grep Network
```
---

### 第二步：关闭无线网卡节能模式（最常见原因）
Ubuntu默认开启了网卡节能，会在闲置时自动休眠断网，这是“断网后自动恢复”的直接原因。

**永久关闭（重启后依然生效，推荐）**
    ```bash
    sudo nano /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
    ```
    将文件中的 `wifi.powersave = 3` 改为 `wifi.powersave = 2`，保存退出（`Ctrl+O` → `Ctrl+X`），然后重启网络管理器：
    ```bash
    sudo systemctl restart NetworkManager
    ```

---

### 第三步：安装适配的第三方驱动（解决网速慢+断网的核心）
开源驱动对RTL8852AE的稳定性和速度优化不足，需要安装社区维护的专用驱动：
1.  先安装依赖工具（如果之前没装`build-essential`，先执行这步）：
    ```bash
    sudo apt update && sudo apt install git build-essential -y
    ```
2.  下载并安装适配驱动（这是目前最稳定的RTL8852AE驱动）：
    ```bash
    git clone https://github.com/lwfinger/rtw89.git
    cd rtw89
    make
    sudo make install
    ```
3.  重启电脑，驱动会自动加载，此时网速和稳定性会大幅提升。

---

### 第四步：优化网络管理器配置（避免频繁漫游断网）
如果仍偶尔断网，是因为网络管理器对弱信号的漫游策略太敏感，可调整：
```bash
sudo nano /etc/NetworkManager/conf.d/99-wifi-roaming.conf
```
粘贴以下内容：
```ini
[connection]
wifi.roaming-strategy=1
wifi.scan-rand-mac-address=no
```
保存退出后，重启网络管理器：
```bash
sudo systemctl restart NetworkManager
```

---
