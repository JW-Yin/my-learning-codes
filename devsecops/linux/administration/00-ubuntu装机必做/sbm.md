# Ubuntu与iPhone 同局域网SMB文件共享（iPhone零安装）完整梳理
**核心**：Ubuntu端配置Samba服务（SMB协议），iPhone用自带「文件」App原生访问，双向传文件，无需在iPhone安装任何软件，全程基于你的实际环境（用户名`jw-yin`、共享文件夹`/home/jw-yin/桌面/shared`）梳理，含**安装配置+全问题解决+优化技巧**，可直接复制命令使用。

## 一、核心准备
1. 确保Ubuntu和iPhone连接**同一局域网（WiFi）**
2. 提前在Ubuntu创建共享文件夹：`mkdir -p /home/jw-yin/桌面/shared`

## 二、Ubuntu端 Samba 完整安装与配置
### 1. 安装Samba核心组件
```bash
sudo apt update && sudo apt install samba samba-common-bin -y
```
### 2. 备份原配置文件（避免误操作）
```bash
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
```
### 3. 编辑Samba主配置文件（关键，含**大文件传输优化+权限映射**）
```bash
sudo nano /etc/samba/smb.conf
```
#### （1）在文件**开头**添加`[global]`段（解决大文件传输“空间不足”误提示）
无则新增，启用SMB3协议+大文件读写优化：
```ini
[global]
    # 适配iPhone，支持大文件传输
    max protocol = SMB3  
    min receivefile size = 16384
    use sendfile = yes
    large readwrite = yes
```
#### （2）在文件**末尾**添加共享配置块`[UbuntuShare]`（解决匿名访问只读问题）
路径为你的实际共享文件夹，添加用户映射确保读写权限：
```ini
[UbuntuShare]
    # 固定你的共享路径，不可改
    path = /home/jw-yin/桌面/shared  
    # 允许iPhone发现该共享
    browseable = yes  
    # 开启读写权限
    read only = no    
    # 允许匿名访问，无需输密码
    guest ok = yes    
    # 匿名用户映射为你的系统用户名
    guest account = jw-yin  
    # 强制所有访问使用你的权限（核心解决只读）
    force user = jw-yin     
    # 新文件默认全权限
    create mask = 0777      
    # 新文件夹默认全权限
    directory mask = 0777   
    # 解决iOS兼容性问题，必加
    vfs objects = catia fruit streams_xattr  
```
#### （3）保存退出nano
`Ctrl+O` → 回车确认 → `Ctrl+X`

### 4. 验证配置语法（必做，避免启动失败）
```bash
sudo testparm
```
**正常输出**：无报错，最后显示`Loaded services file OK.`

### 5. 启动/重启Samba服务+开放防火墙
```bash
# 重启服务（首次启动/配置修改后均需执行）
sudo systemctl restart smbd nmbd
# 开放Samba防火墙端口（一次性操作，永久生效）
sudo ufw allow samba && sudo ufw reload
# 检查服务状态（确认active running，绿色）
sudo systemctl status smbd
```

### 6. 获取Ubuntu局域网IP（iPhone连接用）
```bash
hostname -I  # 简洁输出，如192.168.1.105
```

## 三、iPhone端 原生访问（无安装，和访问Windows共享一致）
1. 打开iPhone自带「**文件**」App
2. 右上角「···」→ 选择「**连接服务器**」
3. 输入地址：`smb://你的UbuntuIP`（如`smb://192.168.1.105`），点击连接
4. 选择「**客人**」（匿名访问，无需输账号密码），直接进入
5. 成功后可见共享名`UbuntuShare`，点击进入即可**双向传文件**（复制/粘贴/新建/删除均支持）

## 四、实战遇到的3个核心问题+解决方案（已踩坑，直接用）
### 问题1：smbd服务启动失败（提示Job failed）
- **核心原因**：配置文件语法错误/共享路径不存在/文件夹权限异常
- **解决步骤**：
  1. 查报错日志定位问题：`sudo systemctl status smbd.service`
  2. 确认共享路径存在：`ls -ld /home/jw-yin/桌面/shared`
  3. 重置文件夹权限：`sudo chmod 777 /home/jw-yin/桌面/shared && sudo chown jw-yin:jw-yin /home/jw-yin/桌面/shared`
  4. 重新验证配置：`sudo testparm`，再重启服务

### 问题2：iPhone能连接但显示**只读**，且看不到shared文件夹
- **核心原因**：Samba匿名用户（guest）默认映射为`nobody`，无访问个人文件夹的权限；或配置路径写错
- **解决步骤**：
  1. 确认配置中`path`是实际路径`/home/jw-yin/桌面/shared`
  2. 确保配置块中添加了`guest account = jw-yin`和`force user = jw-yin`
  3. 重启Samba服务，iPhone端**移除旧共享**后重新连接（长按UbuntuShare→移除）

### 问题3：Ubuntu磁盘空间充足，但iPhone传文件提示**空间不足**
- **核心原因**：Samba默认配置对大文件传输有协议/缓冲区限制，属于**误提示**
- **解决步骤**：
  1. 确保配置文件开头添加了上述`[global]`段的大文件优化配置
  2. 重启Samba服务，iPhone端先传**小文件测试**（如照片），再传大文件

## 五、后续使用优化技巧（提升体验，必看）
### 1. 给Ubuntu设**静态IP**（避免每次连接查IP）
在路由器管理后台，将Ubuntu的**MAC地址**和局域网IP（如192.168.1.105）绑定，永久固定IP，iPhone后续连接无需重新输入。

### 2. 权限优化（更安全，替代777）
若不想给共享文件夹开最高权限777，可改回755，配合`force user = jw-yin`仍能正常读写：
```bash
sudo chmod 755 /home/jw-yin/桌面/shared
```

### 3. 大文件传输提速
- 确保iPhone和Ubuntu均连接**5G WiFi**（避开2.4G WiFi，速度慢易断连）
- 传输前关闭Ubuntu的大文件索引/杀毒软件（若安装），减少系统资源占用

### 4. 新增其他共享文件夹
直接复制`[UbuntuShare]`配置块，修改**共享名**和**path**即可，示例：
```ini
[UbuntuDoc]  # 新共享名
    path = /home/jw-yin/文档  # 新共享路径
    # 以下内容和原配置一致，无需改
    browseable = yes
    read only = no
    guest ok = yes
    guest account = jw-yin
    force user = jw-yin
    create mask = 0777
    directory mask = 0777
    vfs objects = catia fruit streams_xattr
```
修改后执行`sudo testparm && sudo systemctl restart smbd nmbd`，iPhone端刷新即可看到新共享。

## 六、常用快捷命令（日后维护直接复制）
```bash
# 重启Samba服务
sudo systemctl restart smbd nmbd
# 检查Samba服务状态
sudo systemctl status smbd
# 查看Ubuntu局域网IP
hostname -I
# 验证Samba配置语法
sudo testparm
# 重置共享文件夹权限
sudo chmod 777 /home/jw-yin/桌面/shared && sudo chown jw-yin:jw-yin /home/jw-yin/桌面/shared
```