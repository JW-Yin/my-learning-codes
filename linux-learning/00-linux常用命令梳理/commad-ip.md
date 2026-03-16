# 一、先记住：ip 命令的统一格式
```bash
ip [选项] <对象> <动作>
```

最常用 **4 个对象**（记住这4个就够90%场景）：
- `ip link`    → 网卡/接口本身（启停、状态、名字、MTU）
- `ip addr`    → IP 地址（查看、添加、删除）
- `ip route`   → 路由表（网关、默认路由、静态路由）
- `ip neigh`   → ARP 表（邻居设备，替代 `arp`）

---

# 二、最常用：查看信息（必学）
## 1. 查看所有网卡接口（等价 ifconfig -a）
```bash
ip link
```
精简好看版：
```bash
ip -br link
```

## 2. 查看 IP 地址（最常用）
```bash
ip addr
# 简写
ip a
```

## 3. 查看路由表（等价 route -n）
```bash
ip route
# 简写
ip r
```

## 4. 查看 ARP 表（等价 arp -a）
```bash
ip neigh
```

---

# 三、操作网卡（ip link）
## 1. 启停网卡
```bash
# 禁用 eth0（你的可能叫 ens33、enp0s3 之类）
sudo ip link set eth0 down

# 启用 eth0
sudo ip link set eth0 up
```

## 2. 修改 MTU
```bash
sudo ip link set eth0 mtu 1500
```

## 3. 重命名网卡（进阶）
```bash
sudo ip link set eth0 name net0
```

---

# 四、操作 IP 地址（ip addr）【核心】
## 1. 给网卡加一个 IPv4 地址
```bash
sudo ip addr add 192.168.1.100/24 dev eth0
```

## 2. 删除一个 IP
```bash
sudo ip addr del 192.168.1.100/24 dev eth0
```

## 3. 清空网卡所有 IP
```bash
sudo ip addr flush dev eth0
```

---

# 五、操作路由（ip route）
## 1. 添加默认网关
```bash
sudo ip route add default via 192.168.1.1
```

## 2. 添加静态路由
```bash
# 去 10.0.0.0/24 走网关 192.168.1.1
sudo ip route add 10.0.0.0/24 via 192.168.1.1
```

## 3. 删除路由
```bash
sudo ip route del default
sudo ip route del 10.0.0.0/24
```

---

# 六、操作 ARP 表（ip neigh）
## 1. 查看邻居
```bash
ip neigh
```

## 2. 强制刷新一个 ARP 条目
```bash
sudo ip neigh flush 192.168.1.1
```

---

# 七、超实用小选项
```bash
ip -s link           # 显示收发流量统计
ip -c addr           # 彩色输出
ip -4 addr           # 只看 IPv4
ip -6 addr           # 只看 IPv6
ip addr show eth0    # 只看 eth0
```

---

# 八、ifconfig → ip 速查（你直接对照用）
| 功能                  | ifconfig                | ip 命令                          |
|-----------------------|-------------------------|----------------------------------|
| 查看所有接口          | ifconfig -a             | ip a                             |
| 启动网卡              | ifconfig eth0 up        | ip link set eth0 up              |
| 设置IP                | ifconfig eth0 192.168.1.100 netmask 255.255.255.0 | ip addr add 192.168.1.100/24 dev eth0 |
| 查看路由              | route -n                | ip r                             |
| 查看ARP               | arp -a                   | ip neigh                         |

---

# 九、我带你练一套（你复制粘贴跑一遍就会）
假设你的网卡是 `ens33`（Ubuntu 常见）：
```bash
ip -br link
ip a
sudo ip addr add 192.168.1.99/24 dev ens33
ip a
sudo ip addr del 192.168.1.99/24 dev ens33
ip r
ip neigh
```

---
