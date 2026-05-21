好的，我帮你梳理一下：在使用 NetworkManager 的 Linux 机器上，**给某个 Wi-Fi 配置静态 IP，并让系统在发现该 Wi-Fi 信号时自动连接**，完整的操作逻辑如下。

---

## 一、理解 NetworkManager 的“连接”与“自动连接”

- 每个 Wi-Fi 对应一个 **连接配置文件**（connection profile），保存 SSID、安全密码、IP 配置等信息。
- 只要连接配置中的 `connection.autoconnect` 为 `yes`（默认就是），当网卡扫描到该 SSID 并且之前成功连接过，就会**自动连上**。
- 静态 IP 只是修改该连接的 IPv4 设置，不影响自动连接行为。

---

## 二、操作前准备

1. **确认 NetworkManager 正在管理 Wi-Fi**
   ```bash
   nmcli device status
   ```
   看到 `wifi` 设备且状态为 `managed` 即可。

2. **记下 Wi-Fi 的 SSID（就是你要连的那个 Wi-Fi 名字）**，比如 `MyWiFi`。

---

## 三、配置流程（推荐：分情况处理）

### 情况 A：这个 Wi-Fi 之前已经连接过（已存在连接配置）

只需找到对应连接名字，修改为静态 IP，并确保自动连接开启。

```bash
# 1. 列出所有已保存的连接
nmcli connection show

# 假设你看到 NAME 列为 MyWiFi（或 UUID），记下这个名字。
# 2. 修改 IP 配置为静态（替换成你自己的 IP/网关/DNS）
sudo nmcli connection modify "MyWiFi" \
    ipv4.method manual \
    ipv4.addresses 192.168.1.88/24 \
    ipv4.gateway 192.168.1.1 \
    ipv4.dns "114.114.114.114 8.8.8.8"

# 3. 确保自动连接启用（通常默认就是 yes，可显式开启）
sudo nmcli connection modify "MyWiFi" connection.autoconnect yes

# 4. 重新激活连接使静态 IP 生效
sudo nmcli connection down "MyWiFi"
sudo nmcli connection up "MyWiFi"
```

> **提示**：如果你是通过 Wi-Fi 远程连入，`down` 会断开，请确保你已知道新 IP 并能重新连接。

---

### 情况 B：这是一个新 Wi-Fi，从未连接过（没有连接配置）

需要**创建一个连接配置**，同时指定 SSID、密码和静态 IP，并启用自动连接。

```bash
# 一次性创建连接并激活（交互式输入密码不太方便，建议用下面方式）
sudo nmcli device wifi connect "MyWiFi" password "你的WiFi密码" \
    ipv4.method manual \
    ipv4.addresses 192.168.1.88/24 \
    ipv4.gateway 192.168.1.1 \
    ipv4.dns "114.114.114.114 8.8.8.8"
```

这个命令会：
- 创建一个名为 `MyWiFi` 的连接（SSID 也是 MyWiFi）
- 保存密码，自动连接设为 yes
- 立即激活并连上该 Wi-Fi，同时使用静态 IP

> **注意**：如果 SSID 中包含空格或特殊字符，用引号括起来。

---

### 情况 C：已经连上了新 Wi-Fi（但使用 DHCP），想事后改成静态 IP

相当于先有了连接（可能是自动生成的），然后按 **情况 A** 的方法修改它。  
唯一的区别是：你需要先通过 `nmcli connection show` 找到对应的连接名（通常与 SSID 相同），然后执行修改命令。

---

## 四、如何验证自动连接和静态 IP

1. **查看连接属性**
   ```bash
   nmcli connection show "MyWiFi" | grep -E "autoconnect|ipv4.method|ipv4.addresses"
   ```
   输出应包含：
   ```
   connection.autoconnect:  yes
   ipv4.method:             manual
   ipv4.addresses:          192.168.1.88/24
   ```

2. **测试自动连接**  
   断开 Wi-Fi 或重启，只要该 SSID 在范围内，NetworkManager 就会自动连接，IP 保持静态。

3. **恢复 DHCP（如果需要）**
   ```bash
   sudo nmcli connection modify "MyWiFi" ipv4.method auto
   sudo nmcli connection down "MyWiFi" && sudo nmcli connection up "MyWiFi"
   ```

---

## 五、常见问题与补充

- **连接名不是 SSID 怎么办？**  
  有时名称是一串 UUID，可以用 `nmcli connection show` 查看 `WIFI` 字段匹配你的 SSID，然后用 UUID 操作，或重命名：
  ```bash
  sudo nmcli connection modify "旧名字" connection.id "MyWiFi"
  ```

- **自动连接优先级**  
  如果你有多个保存的 Wi-Fi，可用 `connection.autoconnect-priority` 设置优先级，数字越大越优先：
  ```bash
  sudo nmcli connection modify "MyWiFi" connection.autoconnect-priority 10
  ```

- **隐藏 SSID 的 Wi-Fi**  
  创建连接时需要加上 `hidden yes`：
  ```bash
  sudo nmcli connection add type wifi con-name "MyHiddenSSID" ifname wlan0 ssid "MyHiddenSSID" \
       wifi-sec.key-mgmt wpa-psk wifi-sec.psk "密码" \
       ipv4.method manual ipv4.addresses ... hidden yes
  ```

---

总结：对于使用 NetworkManager 的 Linux，**配置静态 IP 和自动连接的关键就是修改或新建连接时，正确设置 `ipv4.method manual` 和 `connection.autoconnect yes`**。按照上面对应的情况操作，一步到位。