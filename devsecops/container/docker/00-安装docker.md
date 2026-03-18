# Docker & Docker Compose 安装与基础配置完整教程（复盘专用）
## 前置说明
- 核心目标：完成Docker引擎、容器运行时、Docker Compose插件的全量安装，配置国内镜像加速，实现免sudo操作，完成环境全链路可用性验证

---

## 一、系统环境初始化（必做第一步）
### 1. 更新系统软件包索引与系统 
**作用**：确保系统包管理器处于最新状态，避免依赖版本冲突导致安装失败
**命令**：
```bash
# 更新软件包索引
sudo apt-get update
# 升级系统已安装的所有软件包（可选但推荐）
sudo apt-get upgrade -y
```

### 2. 卸载系统旧版本Docker（必做，避免冲突）
**作用**：清理系统中可能存在的旧版Docker组件，防止版本冲突
**命令**：
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc -y
```
**避坑提示**：即使从未安装过Docker，执行此命令也无副作用，建议必执行

---

## 二、安装基础依赖包
**作用**：安装后续步骤所需的HTTPS传输、证书验证、文件下载等核心工具
**命令**：
```bash
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg
```
**依赖核心作用**：
- `apt-transport-https`：让apt支持HTTPS协议的软件源
- `ca-certificates`：CA证书包，验证软件源的合法性
- `curl`：文件下载工具
- `software-properties-common`：软件源管理工具
- `gnupg`：GPG密钥加密验证工具

---

## 三、添加Docker官方GPG密钥
**作用**：验证Docker安装包的数字签名，确保安装的是官方未篡改的软件包
**命令**：
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
**避坑提示**：
- 国内网络若下载密钥失败，可切换手机热点重试；
- 命令执行无报错、无额外输出即为成功。

---

## 四、配置Docker软件源（国内优先阿里云镜像源）
**作用**：配置Docker的软件下载源，国内使用阿里云源可大幅提升下载速度，避免官方源访问失败
**命令**：
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
**命令详解**：
- `$(dpkg --print-architecture)`：自动获取系统CPU架构（如amd64/arm64），无需手动修改
- `$(lsb_release -cs)`：自动获取Ubuntu版本代号（如22.04为jammy），自动适配对应系统版本
- `stable`：使用Docker稳定版，生产环境唯一推荐

---

## 五、安装Docker引擎核心组件
### 1. 更新软件包索引（新增源后必做）
```bash
sudo apt-get update
```

### 2. 安装Docker全量组件
**作用**：安装Docker核心服务、命令行工具、容器运行时、构建插件与编排插件
**命令**：
```bash
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
**组件说明**：
- `docker-ce`：Docker社区版核心引擎服务
- `docker-ce-cli`：Docker命令行工具，执行docker命令的核心
- `containerd.io`：OCI标准容器运行时，负责容器的生命周期管理
- `docker-buildx-plugin`：Docker镜像构建扩展工具，支持多架构镜像构建
- `docker-compose-plugin`：Docker Compose V2插件，实现多容器编排（官方推荐，替代旧版docker-compose二进制文件）

---

## 六、Docker安装有效性验证（必做，确认环境可用）
### 1. 验证Docker版本
**命令**：
```bash
sudo docker --version
```
**成功标志**：输出类似如下内容，无报错即安装成功
```
Docker version 27.3.1, build ce12230
```

### 2. 验证Docker服务运行状态
**命令**：
```bash
sudo systemctl status docker
```
**成功标志**：输出中包含`active (running)`，说明Docker服务已正常启动

### 3. 运行测试容器，验证全链路可用性
**作用**：最终验证Docker能否正常拉取镜像、创建容器、运行容器，是环境可用的核心校验
**命令**：
```bash
sudo docker run hello-world
```
**成功标志**：
1. 首次执行会自动拉取`hello-world`镜像；
2. 终端输出包含**`Hello from Docker!`** 字样，说明Docker全链路功能正常。

---

## 七、国内镜像加速配置（国内环境必做，解决镜像拉取慢/失败问题）
### 1. 编辑Docker daemon配置文件
**命令**：
```bash
sudo vim /etc/docker/daemon.json
```

### 2. 写入镜像加速配置
将以下内容完整写入文件，包含国内稳定可用的镜像加速地址：
```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://hub.rat.dev",
    "https://docker.1panel.live",
    "https://registry-1.docker.m.daocloud.io",
    "https://fhayyejh.mirror.aliyuncs.com"
  ]
}
```
**避坑提示**：严格遵循JSON格式，逗号、括号不能错，否则Docker重启会失败

### 3. 重载配置与重启Docker服务
**命令**：
```bash
# 重载系统daemon配置
sudo systemctl daemon-reload
# 可选：配置系统DNS，解决域名解析问题
sudo vim /etc/resolv.conf
# 写入DNS地址：nameserver 223.5.5.5
# 重启Docker服务，使配置生效
sudo systemctl restart docker
```

### 4. 验证加速配置是否生效
**命令**：
```bash
docker info
```
**成功标志**：输出内容的末尾，`Registry Mirrors`字段下出现上面配置的加速地址，说明配置生效

---

## 八、免sudo执行Docker命令配置（可选但强烈推荐）
**背景**：默认情况下，执行docker命令需要加sudo，否则会报`permission denied`权限错误
### 1. 将当前用户加入docker用户组
**命令**：
```bash
sudo usermod -aG docker $USER
```

### 2. 刷新用户组权限（无需重启系统）
**命令**：
```bash
newgrp docker
```
**替代方案**：关闭当前终端，重新打开一个新的终端/SSH连接，权限会自动生效

### 3. 验证免sudo配置是否生效
**命令**：
```bash
docker ps
```
**成功标志**：命令无报错，正常输出容器列表（无容器则输出空表头），说明配置成功，后续无需再加sudo执行docker命令

---

## 九、Docker Compose 验证与兼容配置
### 1. 验证Docker Compose是否安装成功
本教程安装的`docker-compose-plugin`为官方推荐的V2版本，使用`docker compose`（空格，无横杠）命令
**验证命令**：
```bash
docker compose version
```
**成功标志**：输出类似如下内容，无报错即安装成功
```
Docker Compose version v2.29.7
```

### 2. 兼容旧版docker-compose命令（可选）
若习惯使用旧版`docker-compose`（带横杠）命令，可创建软链接实现兼容：
```bash
sudo ln -s /usr/libexec/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose
```
**验证**：执行`docker-compose version`，输出版本信息即生效

---

## 十、Docker服务核心管理命令（复盘必备）
| 命令 | 核心作用 |
|------|----------|
| `sudo systemctl status docker` | 查看Docker服务运行状态 |
| `sudo systemctl start docker` | 启动Docker服务 |
| `sudo systemctl stop docker` | 停止Docker服务 |
| `sudo systemctl restart docker` | 重启Docker服务 |
| `sudo systemctl enable docker` | 设置Docker开机自启（默认已开启） |
| `sudo systemctl disable docker` | 关闭Docker开机自启 |

---

## 十一、新手高频踩坑复盘指南
1. **权限报错问题**：执行docker命令报`permission denied`，要么加sudo，要么完成免sudo配置并刷新终端权限
2. **镜像拉取失败**：国内环境必须配置镜像加速，否则Docker Hub官方源无法访问/速度极慢
3. **配置文件格式错误**：`daemon.json`必须严格遵循JSON格式，写错会导致Docker重启失败
4. **软件源适配问题**：Ubuntu非LTS版本可能出现源找不到的问题，建议使用22.04/24.04等LTS版本
5. **Docker服务未启动**：所有docker命令报错，先执行`sudo systemctl start docker`启动服务

---