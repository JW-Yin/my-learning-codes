
# Docker 环境配置完整流程（从 0 到 hello-world）
## 一、流程总览（先看大图）
1. **清理旧环境**：卸载可能存在的旧版本 Docker，避免冲突；
2. **准备依赖**：更新源、安装基础工具；
3. **建立信任**：添加 Docker 官方 GPG 密钥，验证软件包合法性；
4. **配置官方源**：让系统从 Docker 官方仓库下载安装包；
5. **安装 Docker 引擎**：部署核心组件；
6. **验证安装**：查版本、跑 hello-world 容器，确认能用；
7. **（可选）免 sudo 配置**：提升使用便捷性。

---

## 二、分步复盘（带命令+核心解释）
### 前置说明：适配系统
以下流程**仅适用于 Ubuntu 22.04**（你的系统），其他发行版需调整。

---

### 步骤 1：卸载旧版本（如果有）
**目的**：清理系统中可能存在的旧 Docker 组件，避免版本冲突。
**命令**：
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```
**核心解释**：
- 即使没装过 Docker，执行这个命令也没问题（不会报错），建议先跑一遍。

---

### 步骤 2：更新源 + 安装基础依赖
**目的**：让系统能访问最新的软件包，并安装后续步骤需要的工具（比如 `curl` 用于下载、`gnupg` 用于验证密钥）。
**命令**：
```bash
# 1. 更新 apt 源
sudo apt-get update

# 2. 安装基础依赖
sudo apt-get install ca-certificates curl gnupg
```

---

### 步骤 3：添加 Docker 官方 GPG 密钥
**目的**：验证 Docker 官方安装包的合法性（防止安装恶意软件）。
**命令**：
```bash
# 1. 创建密钥存储目录（如果不存在）
sudo install -m 0755 -d /etc/apt/trusted.gpg.d

# 2. 下载并导入 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker.gpg

# 3. 给密钥文件设置读权限
sudo chmod a+r /etc/apt/trusted.gpg.d/docker.gpg
```

---

### 步骤 4：配置 Docker 官方软件源
**目的**：让系统从 Docker 官方仓库下载安装包（保证版本最新、最正规）。
**命令**：
```bash
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/trusted.gpg.d/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
**核心解释**：
- `$(dpkg --print-architecture)`：自动获取你的系统架构（比如 amd64）；
- `$(. /etc/os-release && echo "$VERSION_CODENAME")`：自动获取 Ubuntu 版本代号（22.04 是 `jammy`），不用手动改；
- `stable`：使用 Docker 的稳定版（推荐）。

---

### 步骤 5：安装 Docker 引擎（核心步骤）
**目的**：部署 Docker 的核心组件（Docker 服务、命令行工具、容器运行时等）。
**命令**：
```bash
# 1. 再次更新 apt 源（因为刚加了 Docker 官方源）
sudo apt-get update

# 2. 安装 Docker 引擎及配套工具
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
**核心解释**：
- `docker-ce`：Docker 社区版（核心服务）；
- `docker-ce-cli`：Docker 命令行工具（你敲 `docker` 命令用的就是这个）；
- `containerd.io`：容器运行时（负责管理容器生命周期）；
- `docker-buildx-plugin`：构建镜像的扩展工具；
- `docker-compose-plugin`：编排多容器的工具（后续进阶用）。

---

### 步骤 6：验证安装（必须做，确认能用）
#### 6.1 查看 Docker 版本
**命令**：
```bash
docker --version
```
**成功标志**：输出类似 `Docker version 26.x.x, build xxx`。

#### 6.2 运行官方测试容器（hello-world）
**命令**：
```bash
sudo docker run hello-world
```
**成功标志**：
- 第一次执行会自动从 Docker Hub 拉取 `hello-world` 镜像；
- 最后出现一大段文字，包含 **`Hello from Docker!`**。
→ 说明：Docker 能正常拉取镜像、创建容器、运行容器，环境完全正常！

---

### 步骤 7：（可选但强烈推荐）免 sudo 使用 Docker
**背景**：默认操作 Docker 需要加 `sudo`（比如 `sudo docker ps`），比较麻烦。
**目的**：给当前用户添加 Docker 组权限，以后不用每次输 `sudo`。
**命令**：
```bash
# 1. 把当前用户加入 docker 组
sudo usermod -aG docker $USER

# 2. 必须做：退出终端，重新打开一个新终端（或重新登录）
```
**验证**：
重新打开终端后，执行：
```bash
docker ps
```
→ 不报错就说明配置成功，以后用 Docker 不用加 `sudo` 了。

---

## 三、复盘核心关键点（必记）
1. **必须按顺序来**：清理旧版本 → 装依赖 → 加密钥 → 配源 → 安装 → 验证；
2. **GPG 密钥和官方源是安全保障**：确保安装的是 Docker 官方的稳定版，不是第三方修改的；
3. **验证是必须的**：只有跑通 `hello-world`，才能确认 Docker 真的能用；
4. **免 sudo 配置后必须重启终端**：否则权限不生效。

---

