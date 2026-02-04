# Ubuntu 网络配置梳理

## 一、更换Ubuntu下载源（清华源）
### 作用
提升软件下载/更新速度，解决官方源访问慢、卡顿的问题。
### 操作步骤
1. 备份原有源文件（防止修改出错可恢复）：
   ```bash
   sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
   ```

2. 编辑源配置文件：
   ```bash
   sudo nano /etc/apt/sources.list
   ```

3. 将文件内原有内容替换为**对应Ubuntu版本的清华源**：
    ```bash
    deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
    deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
    deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
    deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
    ```

4. 更新源缓存（使新源生效）：
   ```bash
   sudo apt update
   ```
5. 升级系统已安装包：
   ```bash
   sudo apt upgrade
   ```



## 二、关闭无线网卡节能模式（解决偶尔断网问题）
### 问题原因
Ubuntu默认开启无线网卡节能，闲置时网卡自动休眠，导致“断网后自动恢复”或间歇性断网，这是该类断网的最常见诱因。
### 操作方式（永久关闭，重启后仍生效，推荐）
1. 编辑网卡节能配置文件：
   ```bash
   sudo nano /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf
   ```
2. 修改配置项：将文件中 `wifi.powersave = 3` 改为 `wifi.powersave = 2`；
3. 保存并退出nano编辑器：按 `Ctrl+O` 保存 → 按 `Ctrl+X` 退出；
4. 重启网络管理器使配置生效：
   ```bash
   sudo systemctl restart NetworkManager
   ```
