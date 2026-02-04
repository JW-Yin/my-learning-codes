# Ubuntu 22.04 Miniconda 安装配置
## 适用场景
- 系统：Ubuntu 22.04（x86_64架构；ARM架构需替换下载链接后缀为 `Linux-aarch64`）
- 优化：全程用清华镜像加速，复刻Windows Miniconda使用习惯

## 安装配置核心步骤
### 步骤1：安装下载工具（可选，已装跳过）
```bash
sudo apt install wget -y  # 提示wget未找到时执行
```

### 步骤2：下载Miniconda安装包（清华源+断点续传）
```bash
wget -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
- 断点续传：下载中断后重新执行上述命令即可续传

### 步骤3：安装Miniconda（二选一）
#### 方式1：静默安装（无交互，推荐）
```bash
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3
```
- 关键：`-b`（静默）、`~/miniconda3`（用户级路径，避免权限问题）
- 成功标识：终端输出 `installation finished.`

#### 方式2：交互安装（按提示操作）
```bash
chmod +x Miniconda3-latest-Linux-x86_64.sh  # 添加执行权限
./Miniconda3-latest-Linux-x86_64.sh
```
- 交互关键：协议选`yes`、安装路径默认、初始化选`yes`

### 步骤4：配置conda环境变量（立即生效）
```bash
echo ". ~/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc && source ~/.bashrc
```
- 新终端提示`conda未找到`：执行 `source ~/.bashrc` 重新加载

### 步骤5：配置conda清华镜像源
```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch
conda config --set show_channel_urls yes
```

### 步骤6：配置pip清华镜像源
```bash
mkdir -p ~/.pip  # 创建配置目录
nano ~/.pip/pip.conf  # 编辑配置文件
```
在编辑器中粘贴以下内容，按 `Ctrl+O`→回车→`Ctrl+X` 保存退出：
```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
```

## 验证配置（必做）
| 验证项                | 命令                          | 预期结果                          |
|-----------------------|-------------------------------|-----------------------------------|
| conda命令可用         | `conda --version`             | 输出版本号（如conda 24.9.0）|
| conda镜像源生效       | `conda config --show-sources` | 显示清华源地址，无海外源          |
| pip镜像源生效         | `pip config list`             | 显示清华pip源地址                 |

## 核心基础用法（与Windows一致）
```bash
conda --version                # 查看conda版本
conda create -n py310 python=3.10 -y  # 创建Python3.10环境（py310为环境名）
conda activate py310           # 激活环境
conda install numpy pandas -y  # 安装包（示例）
conda deactivate               # 退出环境
conda env list                 # 查看所有环境
```

## 避坑注意事项
1. 架构适配：ARM架构需替换下载链接中`Linux-x86_64`为`Linux-aarch64`；
2. 权限问题：安装路径选`~/miniconda3`（用户级），无需sudo；
3. 源的区别：conda源仅作用于`conda install`，pip源仅作用于`pip install`，需分别配置；
4. conda命令失效：新终端提示未找到，执行`source ~/.bashrc`重新加载环境变量；
5. 断点续传：下载安装包中断，重新执行`wget -c 下载链接`即可。