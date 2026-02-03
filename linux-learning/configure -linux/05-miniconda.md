# Linux（Ubuntu）Miniconda 安装配置梳理（复习版）
## 适用场景
Ubuntu x86_64 架构、大陆用户（全程清华镜像）、复刻 Windows Miniconda 使用习惯。

## 核心流程（按执行顺序）
### 步骤1：安装基础下载工具（可选，已装则跳过）
**目的**：获取 `wget` 工具用于下载 Miniconda 安装包
```bash
sudo apt install wget -y
```

### 步骤2：国内镜像下载 Miniconda 安装包
**目的**：通过清华源断点续传下载，规避海外下载慢/超时问题
```bash
wget -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

### 步骤3：静默安装 Miniconda（指定路径）
**目的**：无弹窗自动安装，安装路径选用户主目录（无权限问题）
```bash
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3
```
- 关键参数：`-b`（静默安装）、`-p ~/miniconda3`（指定安装路径）；
- 成功标识：终端输出 `installation finished.`。

### 步骤4：配置 conda 环境变量
**目的**：让终端识别 `conda` 命令，且配置立即生效（无需重启终端）
```bash
echo ". ~/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc && source ~/.bashrc
```

### 步骤5：配置 conda 国内镜像源
**目的**：加速 `conda install` 安装包，全程走清华国内源
```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch
conda config --set show_channel_urls yes
```

### 步骤6：单独配置 pip 国内镜像源（核心补充）
**目的**：加速 `pip install` 安装包（conda 源 ≠ pip 源，需单独配置）
```bash
# 1. 创建 pip 配置目录
mkdir -p ~/.pip
# 2. 编辑 pip 配置文件
nano ~/.pip/pip.conf
```
在 `nano` 编辑器中粘贴以下内容：
```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
```
保存退出：`Ctrl+O` → 按回车确认文件名 → `Ctrl+X`。

## 必做验证（确认全部配置生效）
### 验证1：conda 命令可用
```bash
conda --version
```
- 预期：输出版本号（如 `conda 24.9.0`，版本号可不同，有输出即正常）。

### 验证2：conda 镜像源配置成功
```bash
conda config --show-sources
```
- 预期：显示清华镜像源地址，无海外源。

### 验证3：pip 镜像源配置成功
```bash
pip config list
```
- 预期：显示 `global.index-url='https://pypi.tuna.tsinghua.edu.cn/simple'` 等清华源信息。

## 核心基础用法（与 Windows 一致）
```bash
# 查看 conda 版本
conda --version
# 创建虚拟环境（例：py310，Python3.10）
conda create -n py310 python=3.10 -y
# 激活虚拟环境
conda activate py310
# 安装包（例：numpy + pandas）
conda install numpy pandas -y
# 退出虚拟环境
conda deactivate
# 查看所有已创建的环境
conda env list
```

## 避坑注意事项（复习重点）
1. 架构适配：x86_64 用默认下载链接；ARM 架构（国产芯片）需将链接中 `Linux-x86_64` 替换为 `Linux-aarch64`；
2. 断点续传：下载安装包中断时，重新执行 `wget -c 下载链接` 即可续传；
3. conda 命令失效：新开终端提示“conda：未找到命令”，执行 `source ~/.bashrc` 重新加载环境变量；
4. 权限问题：安装路径 `~/miniconda3` 为用户级路径，无需 `sudo`，避免权限异常；
5. 源的区别：conda 源仅作用于 `conda install`，pip 源仅作用于 `pip install`，需分别配置。