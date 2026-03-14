# dig 命令完整学习指南
dig 全称 **Domain Information Groper**，是类Unix系统中专业级DNS域名解析查询工具，核心用于DNS故障排查、域名记录验证、解析链路追踪，是网络运维、域名管理的核心工具，功能和灵活性远超传统的`nslookup`。

---

## 一、前置准备：安装dig
dig 来自DNS工具集，不同系统安装命令如下（你使用的Ubuntu 22.04优先看第一条）：
| 系统系列 | 安装命令 |
|----------|----------|
| Debian/Ubuntu 22.04/20.04 | `sudo apt update && sudo apt install dnsutils` |
| RHEL/CentOS/Rocky/AlmaLinux | `sudo dnf install bind-utils` |
| macOS | 系统自带，缺失可执行 `xcode-select --install` |
| Windows | 需安装WSL子系统或BIND官方工具包 |

安装完成后，执行 `dig -v` 可查看版本，确认安装成功。

---

## 二、基础语法与最简用法
### 标准语法
```bash
dig [全局选项] [@DNS服务器地址] [域名] [记录类型] [查询选项]
```
核心字段说明：
1.  `@DNS服务器地址`：可选，指定查询用的DNS服务器IP/域名，不填则使用系统`/etc/resolv.conf`的默认DNS
2.  `域名`：待查询的目标域名
3.  `记录类型`：可选，指定DNS记录类型，默认查询A记录（IPv4地址）
4.  选项区分：`-`开头为**全局选项**，`+`开头为**查询选项**

### 最简入门示例
```bash
dig baidu.com
```
该命令会使用系统默认DNS，查询`baidu.com`的A记录（IPv4地址），输出完整的DNS查询报文。

---

## 三、核心：默认输出完整解读
新手最容易困惑的是dig的默认输出，我们以`dig baidu.com`为例，逐段拆解含义：
```
; <<>> DiG 9.18.1-1ubuntu1.3-Ubuntu <<>> baidu.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;baidu.com.			IN	A

;; ANSWER SECTION:
baidu.com.		300	IN	A	110.242.68.66
baidu.com.		300	IN	A	39.156.66.10

;; Query time: 12 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Sat Mar 14 10:00:00 CST 2026
;; MSG SIZE  rcvd: 81
```

| 输出段落 | 核心含义 | 关键细节 |
|----------|----------|----------|
| 头部Header段 | 查询状态与标志位 | `status: NOERROR`=查询成功；<br>常见错误：`NXDOMAIN`(域名不存在)、`SERVFAIL`(DNS查询失败)、`REFUSED`(查询被拒绝)<br>`flags: qr rd ra`：qr=响应报文、rd=期望递归、ra=服务器支持递归 |
| QUESTION SECTION | 查询问题段 | 明确本次查询的目标：`baidu.com.`的IN(互联网类)A记录，结尾`.`代表根域名（FQDN完全合格域名标准格式） |
| ANSWER SECTION | 核心应答段 | 逐列含义：<br>1. 目标域名<br>2. TTL(缓存存活时间，单位秒)<br>3. IN(固定互联网类)<br>4. 记录类型<br>5. 记录值（IP/域名等） |
| 底部统计段 | 查询元数据 | 查询耗时、使用的DNS服务器地址+端口、查询时间、返回报文大小<br>Ubuntu默认DNS为`127.0.0.53#53`，是systemd-resolved本地DNS服务 |

> 补充：`AUTHORITY SECTION`(权威段)返回域名的权威DNS服务器，`ADDITIONAL SECTION`(附加段)返回权威DNS的IP，缓存查询时这两段可能为空。

---

## 四、高频常用参数与实战示例
严格遵循规则：**每个参数均标注英文缩写来源**，方便你理解记忆。

### （一）基础查询类
#### 1. 指定DNS服务器查询
- 用途：绕过系统默认DNS，排查本地DNS缓存/配置问题，验证公共DNS的解析结果
- 语法：`dig @DNS服务器IP 域名`
- 示例：
  ```bash
  # 用谷歌公共DNS查询baidu.com
  dig @8.8.8.8 baidu.com
  # 用国内114DNS查询
  dig @114.114.114.114 baidu.com
  ```

#### 2. 指定DNS记录类型查询（`-t` = `--type`，指定记录类型）
- 用途：查询域名的不同类型DNS记录，是dig最核心的功能之一
- 语法：`dig -t 记录类型 域名`（`-t`可省略，直接写记录类型）
- 常用记录类型速查表：
  | 记录类型 | 用途 |
  |----------|------|
  | A | 域名对应的IPv4地址，最常用 |
  | AAAA | 域名对应的IPv6地址 |
  | MX | 邮件交换记录，用于邮箱收发 |
  | NS | 域名的权威DNS服务器记录 |
  | TXT | 文本记录，用于域名验证、SPF防垃圾邮件、DKIM签名 |
  | CNAME | 别名记录，将域名指向另一个域名 |
  | SOA | 起始授权记录，域名的核心配置（主DNS、刷新规则等） |
- 示例：
  ```bash
  # 查询QQ邮箱的MX记录
  dig -t MX qq.com
  # 查询域名的TXT验证记录
  dig baidu.com TXT
  # 查询域名的权威DNS服务器
  dig -t NS baidu.com
  ```

#### 3. 精简输出，只看核心结果（`+short` = 精简输出格式）
- 用途：过滤冗余报文，只返回最终的记录值，脚本调用、快速查询必备
- 示例：
  ```bash
  # 只返回baidu.com的IPv4地址
  dig +short baidu.com
  # 只返回MX记录的精简结果
  dig +short MX qq.com
  ```

### （二）进阶排查类
#### 4. 反向DNS解析（`-x` = `--reverse`，反向查询）
- 用途：通过IP地址反查对应的PTR记录（域名），常用于邮件服务器反垃圾验证、IP归属排查
- 语法：`dig -x IP地址`
- 示例：
  ```bash
  # 反查阿里云DNS的IP对应的域名
  dig -x 223.5.5.5
  ```
> 说明：该命令会自动将IP转换为反向解析的`in-addr.arpa`格式，无需手动拼接。

#### 5. 追踪DNS完整解析链路（`+trace` = 追踪根到权威的委托路径）
- 用途：DNS故障排查的终极手段，完整展示**根域名服务器 → 顶级域服务器 → 二级域权威服务器 → 最终记录**的全链路解析过程，精准定位哪一级DNS出了问题
- 示例：
  ```bash
  dig +trace baidu.com
  ```
> 说明：开启`+trace`后，dig会关闭递归查询，逐级迭代查询，完整展示每一跳的DNS服务器和返回结果。

#### 6. 强制使用TCP协议查询（`+tcp` = 强制TCP协议查询）
- 背景：dig默认使用UDP协议，DNS报文超过512字节会被截断，导致结果不完整；区域传送、DNSSEC查询必须使用TCP
- 语法：`dig +tcp @DNS服务器 域名`
- 示例：
  ```bash
  # 强制TCP查询，解决报文截断问题
  dig +tcp @8.8.8.8 baidu.com
  ```
> 对应参数`+udp`：强制使用UDP协议（默认开启）。

#### 7. 指定DNS端口查询（`-p` = `--port`，指定端口号）
- 用途：DNS默认端口为53，自定义DNS服务使用非标准端口时，用该参数指定
- 语法：`dig -p 端口号 @DNS服务器 域名`
- 示例：
  ```bash
  # 用5353端口查询本地DNS服务器
  dig -p 5353 @192.168.1.1 baidu.com
  ```

---

## 五、高频实战场景速查
| 业务需求 | 直接可用的命令 |
|----------|----------------|
| 快速获取域名的IPv4地址 | `dig +short baidu.com` |
| 用指定公共DNS排查解析问题 | `dig @114.114.114.114 baidu.com` |
| 查看域名的邮件服务器配置 | `dig -t MX qq.com` |
| 反向解析IP对应的域名 | `dig -x 8.8.8.8` |
| 追踪域名完整解析链路，定位故障 | `dig +trace baidu.com` |
| 解决UDP报文截断导致的查询不全 | `dig +tcp @8.8.8.8 baidu.com` |
| 查看域名的TXT验证/SPF记录 | `dig -t TXT baidu.com` |

---

## 六、避坑指南与常见问题
1.  **NXDOMAIN错误**：`status: NXDOMAIN` 表示该域名不存在，或顶级域服务器无该域名的有效记录
2.  **UDP截断问题**：输出提示`Truncated`，说明UDP报文超过长度限制，必须加`+tcp`用TCP协议查询
3.  **TTL值说明**：应答中的TTL是**剩余缓存时间**，不是域名原始配置的TTL，查原始TTL需直接访问域名的权威DNS服务器
4.  **ANY查询限制**：绝大多数公共DNS（8.8.8.8、114.114.114.114）禁用了`ANY`查询（防DNS放大攻击），查不到所有记录属于正常现象
5.  **CNAME记录说明**：查询`www.baidu.com`会先返回CNAME别名记录，最终解析到别名对应的A记录，属于正常的域名别名配置

---

## 七、学习路径建议
1.  入门：先练熟`+short`快速查IP、指定DNS服务器查询，看懂核心应答段
2.  进阶：掌握不同记录类型的查询、反向解析、TCP强制查询
3.  精通：用好`+trace`链路追踪，能独立定位DNS解析故障的节点