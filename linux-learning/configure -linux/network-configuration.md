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

# 安装pig_cha
1. 去这里注册账号并且下载`.deb`包：`https://link.vtlovenet.xyz/register?share_id=5799cb22-c501-4fe2-8414-786e3b5aa3f2&lang=zh`
1. `sudo apt install libappindicator3-1 -y`
1. `sudo dpkg -i ViewTurboLite_amd64.deb`

# 安装clash
1. 先去这里注册账号并登陆`https://ikuuu.nl/auth/register?code=ei89`
1. 下载二进制文件：
    ```bash
    mkdir ~/clash; cd ~/clash;
    wget "https://e1uoq.big-files.make-w0rld-static.club:8000/file/ikuuu-static-release/clash-linux/clash-linux-1.0.1/clash-linux-amd64.gz" -O clash-linux-amd64.gz;
    gzip -d clash-linux-amd64.gz;
    mv clash-linux-amd64 clash;
    chmod +x clash;
    ```
1. 到`~clash`目录下执行`wget -O config.yaml "https://pcq7y.no-mad-world.club/link/Lnhw8YmdYo7on5BF?clash=3"`
1. 执行`./clash -d .`启动代理
1. 访问`https://clash.razord.top/#/proxies`配置代理（弹出窗口点添加确定）
1. 启动系统代理


# 一键启动Clash+配置系统代理 自动化脚本（Ubuntu专属）
可以通过**Shell脚本**将「切换目录、启动Clash、设置系统手动代理」三步操作整合为一键执行，完美解决手动操作繁琐的问题。以下提供**可直接使用的成品脚本**，适配Ubuntu桌面版（GNOME环境，你手动设置代理的界面就是GNOME默认界面），包含**启动脚本**和配套的**停止代理脚本**（方便后续关闭），步骤简单、直接可用。

## 一、核心实现原理
1. 脚本自动切换到`~/clash`目录，后台启动Clash（避免终端关闭导致Clash退出）；
2. 通过Ubuntu**原生命令行工具`gsettings`** 直接修改系统网络代理配置（替代手动点设置界面），无需图形化操作；
3. 做了**进程冲突、文件检查**，避免重复启动Clash导致端口占用，同时防止脚本执行报错。

## 二、第一步：创建Clash一键启动脚本
### 1. 新建脚本文件
在终端执行以下命令，新建名为`clash-start.sh`的脚本文件（建议放在`~/clash`目录，方便管理）：
```bash
cd ~/clash && touch clash-start.sh
```

### 2. 写入脚本内容
执行以下命令编辑脚本，将下方成品代码写入：
```bash
nano ~/clash/clash-start.sh
```
复制粘贴以下**完整代码**（直接全选复制即可，无需修改，Clash默认端口已适配）：
```bash
#!/bin/bash
# Clash一键启动+自动配置系统代理 脚本（Ubuntu GNOME）
# Clash默认代理端口：HTTP/HTTPS=7890，SOCKS5=7891（无需修改，Clash默认配置）
PROXY_PORT_HTTP=7890
PROXY_PORT_SOCKS=7891
CLASH_DIR=~/clash
CLASH_BIN=$CLASH_DIR/clash

# 步骤1：检查Clash可执行文件是否存在
if [ ! -f "$CLASH_BIN" ]; then
    echo "❌ 错误：未找到Clash可执行文件！路径：$CLASH_BIN"
    echo "请确认Clash文件在~/clash目录下，且文件名为clash"
    exit 1
fi

# 步骤2：杀死已运行的Clash进程（避免端口占用）
if pgrep -x "clash" > /dev/null; then
    echo "🔍 发现已有Clash进程在运行，正在关闭..."
    pkill -x "clash"
    sleep 1 # 等待进程完全退出
fi

# 步骤3：切换到Clash目录，后台启动Clash（指定工作目录为当前目录）
echo "🚀 正在后台启动Clash..."
cd "$CLASH_DIR" || exit 1 # 切换目录失败则退出
nohup ./clash -d . > nohup.clash.log 2>&1 &
# nohup+&：后台运行，终端关闭不退出；日志输出到nohup.clash.log，方便排查问题

# 步骤4：等待Clash启动（避免代理配置先于Clash启动导致失效）
sleep 2

# 步骤5：通过gsettings配置系统手动代理（替代图形化操作）
echo "⚙️ 正在自动配置系统网络代理..."
gsettings set org.gnome.system.proxy mode 'manual'          # 代理模式改为「手动」
gsettings set org.gnome.system.proxy.http host '127.0.0.1' # HTTP代理地址（本地回环）
gsettings set org.gnome.system.proxy.http port "$PROXY_PORT_HTTP" # HTTP代理端口
gsettings set org.gnome.system.proxy.https host '127.0.0.1' # HTTPS代理地址
gsettings set org.gnome.system.proxy.https port "$PROXY_PORT_HTTP" # HTTPS代理端口
gsettings set org.gnome.system.proxy.socks host '127.0.0.1' # SOCKS5代理地址
gsettings set org.gnome.system.proxy.socks port "$PROXY_PORT_SOCKS" # SOCKS5代理端口
gsettings set org.gnome.system.proxy.socks port "$PROXY_PORT_SOCKS"
# 让所有协议都使用本地代理，与手动设置的「手动代理」完全一致

# 步骤6：验证启动结果
if pgrep -x "clash" > /dev/null; then
    echo "✅ 操作完成！Clash已后台启动，系统代理已自动设置为手动模式"
    echo "📌 日志文件：$CLASH_DIR/nohup.clash.log（启动失败可查看此日志）"
    echo "📌 停止代理：执行配套的 clash-stop.sh 脚本即可"
else
    echo "❌ 启动失败！请查看日志：$CLASH_DIR/nohup.clash.log"
fi
```

### 3. 给脚本添加可执行权限
脚本必须添加**执行权限**才能运行，执行以下命令：
```bash
chmod +x ~/clash/clash-start.sh
```

## 三、第二步：创建配套停止脚本（必装，方便后续关闭）
启动代理后，需要一键关闭时，用这个脚本可**停止Clash进程+恢复系统代理为「禁用」**，避免忘记关代理导致网络异常，操作同启动脚本：

### 1. 新建停止脚本文件
```bash
cd ~/clash && touch clash-stop.sh
```

### 2. 写入脚本内容
```bash
nano ~/clash/clash-stop.sh
```
复制粘贴以下完整代码：
```bash
#!/bin/bash
# Clash一键停止+恢复系统代理为禁用 脚本（Ubuntu GNOME）

# 步骤1：杀死Clash进程
if pgrep -x "clash" > /dev/null; then
    echo "🔌 正在停止Clash进程..."
    pkill -x "clash"
    sleep 1
else
    echo "🔍 未发现运行中的Clash进程"
fi

# 步骤2：恢复系统代理为「禁用」模式（与手动操作一致）
echo "⚙️ 正在恢复系统网络代理为禁用..."
gsettings set org.gnome.system.proxy mode 'none'

# 步骤3：提示完成
echo "✅ 操作完成！Clash已停止，系统代理已禁用，网络恢复正常"
```

### 3. 添加可执行权限
```bash
chmod +x ~/clash/clash-stop.sh
```

## 四、一键使用方法（核心操作）
### 🔹 启动Clash+开启代理（替代手动所有操作）
**终端任意目录**执行以下命令，一键完成所有操作：
```bash
~/clash/clash-start.sh
```
执行后终端会输出提示，看到`✅ 操作完成`即表示成功，无需再做任何手动设置！

### 🔹 停止Clash+关闭代理（使用完必执行）
**终端任意目录**执行以下命令，恢复网络正常：
```bash
~/clash/clash-stop.sh
```

## 五、进阶优化：让脚本在「任意目录」直接执行（可选）
如果觉得输入`~/clash/xxx.sh`麻烦，可以将脚本软链接到**系统可执行目录**`/usr/local/bin`（就是你之前移动clash的目录），实现**直接输入脚本名**即可运行，步骤如下：
```bash
# 给启动脚本创建软链接
sudo ln -s ~/clash/clash-start.sh /usr/local/bin/clash-start
# 给停止脚本创建软链接
sudo ln -s ~/clash/clash-stop.sh /usr/local/bin/clash-stop
```
创建后，**终端任意目录**直接执行以下命令即可，更便捷：
```bash
# 一键启动
clash-start
# 一键停止
clash-stop
```

## 六、关键说明&常见问题解决
### 1. Clash端口说明
脚本中使用的是Clash**默认端口**：`HTTP/HTTPS=7890`、`SOCKS5=7891`，如果你的Clash修改过端口（如在配置文件`config.yaml`中修改），只需打开`clash-start.sh`，修改开头的`PROXY_PORT_HTTP`和`PROXY_PORT_SOCKS`为你的自定义端口即可。

### 2. 日志文件查看
Clash的启动日志、报错信息都会输出到`~/clash/nohup.clash.log`，如果启动失败（如提示端口占用、配置文件错误），执行以下命令查看日志排查：
```bash
cat ~/clash/nohup.clash.log
```

### 3. 脚本适配性
此脚本仅适配**Ubuntu桌面版（GNOME环境）**（你手动设置代理的界面就是GNOME），如果是其他桌面环境（如KDE、XFCE），代理配置命令会不同，可留言补充环境，我会更新适配版本。

### 4. 重复执行脚本无影响
脚本内置了**进程检查**，重复执行`clash-start.sh`会先关闭已运行的Clash进程，再重新启动，不会导致端口占用，放心使用。

## 总结
1. 核心实现：通过`Shell脚本`整合所有操作，用`gsettings`替代手动图形化配置代理，用`nohup &`让Clash后台运行；
2. 一键使用：创建`clash-start.sh`（启动+开代理）和`clash-stop.sh`（停止+关代理），添加执行权限后即可运行；
3. 进阶优化：创建软链接到`/usr/local/bin`，实现终端任意目录直接输入`clash-start`/`clash-stop`执行；
4. 关键保障：内置文件检查、进程冲突处理、日志输出，方便排查问题，使用更稳定。
