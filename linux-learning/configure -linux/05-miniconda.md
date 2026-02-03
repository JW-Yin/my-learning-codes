# Linux（Ubuntu）下 Miniconda 完整安装配置梳理（大陆适配版）
**适用场景**：Ubuntu 系统（x86_64 主流架构）、大陆用户（全程用清华国内镜像，规避海外下载慢/超时）、复刻 Windows 下 Miniconda 使用习惯，所有命令可直接复制执行，步骤清晰可追溯。

### 前置说明
Miniconda 是跨平台 Python 环境管理工具，Linux 安装后**所有命令（conda create/activate/install）与 Windows 完全一致**，无需更改使用习惯；以下步骤含「安装+环境变量+国内镜像源」核心配置，解决所有基础使用问题。

## 一、前期准备：安装基础下载工具（若未安装）
下载 Miniconda 安装包需要 `wget` 工具，终端执行以下命令安装（若已安装可跳过）：
```bash
sudo apt install wget -y
```

## 二、步骤1：国内镜像下载 Miniconda 安装包（清华源，推荐）
选用**清华大学开源镜像站**（更新及时、速度最快），带断点续传参数 `-c`（下载中断后重新执行可继续，无需从头开始），终端执行：
```bash
# 下载最新版 Miniconda3（Linux x86_64，默认适配 Python3.10+，稳定版）
wget -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

## 三、步骤2：静默安装 Miniconda（无弹窗、指定路径）
采用**静默安装模式**（避免手动弹窗选择），指定安装路径为用户主目录 `~/miniconda3`（无权限问题，符合Windows默认路径逻辑），终端执行：
```bash
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3
```
### 关键参数说明
- `-b`：静默安装，无需手动按回车/确认 `yes`，全程自动执行；
- `-p ~/miniconda3`：指定安装路径（主目录下的 miniconda3 文件夹），后续可通过该路径找到conda安装目录。
### 安装成功标识
终端最后输出 `installation finished.` 即表示安装完成。

## 四、步骤3：配置环境变量（让终端识别 conda 命令，核心）
安装后终端默认无法识别 `conda` 命令，需将conda写入系统环境变量文件 `~/.bashrc`，并让配置**立即生效**（无需重启终端/系统），终端执行：
```bash
# 写入环境变量 + 立即加载生效，一步完成
echo ". ~/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc && source ~/.bashrc
```
### 核心作用
- `echo ... >> ~/.bashrc`：将conda的环境配置追加到系统默认环境变量文件，永久生效；
- `source ~/.bashrc`：让当前终端立即加载更新后的环境变量，避免关闭重开终端的麻烦。

## 五、步骤4：配置国内conda镜像源（加速后续包安装，大陆必做）
默认conda走海外源，安装Python包（numpy/pandas等）时速度慢、易超时，**一键配置清华镜像源**（全程走国内通道），终端执行：
```bash
# 1. 添加清华官方conda镜像通道（覆盖默认海外源）
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch
# 2. 显示下载包时的源地址（方便验证是否使用国内镜像）
conda config --set show_channel_urls yes
```

## 六、核心验证：确认安装+配置全部成功（两步必做）
执行以下命令，均出现预期输出即表示整个流程配置完成，可正常使用。
### 验证1：Miniconda安装成功（conda命令可用）
```bash
conda --version
```
**预期输出**：输出版本号（如 `conda 24.9.0`，版本号可不同，有输出即正常）。

### 验证2：国内镜像源配置成功
```bash
conda config --show-sources
```
**预期输出**：显示配置的清华镜像源地址（含 `https://mirrors.tuna.tsinghua.edu.cn/...`），无其他海外源即可。

## 七、后续基础用法（与Windows Anaconda Prompt完全一致，快速上手）
配置完成后，所有conda命令与Windows下无差异，核心常用命令如下：
```bash
# 1. 查看conda版本（验证用）
conda --version
# 2. 创建虚拟环境（例：创建名为py310、Python3.10的环境）
conda create -n py310 python=3.10 -y
# 3. 激活虚拟环境（核心，和Windows一致）
conda activate py310
# 4. 安装Python包（例：安装numpy、pandas）
conda install numpy pandas -y
# 5. 退出当前虚拟环境
conda deactivate
# 6. 查看所有已创建的虚拟环境
conda env list
```

## 八、关键注意事项（日后回顾避坑）
1. 架构匹配：上述步骤仅适用于 **Linux x86_64 架构**（主流笔记本/台式机），若为ARM架构（如国产芯片），需将下载链接中的 `Linux-x86_64` 替换为 `Linux-aarch64`；
2. 断点续传：若下载安装包时网络中断，重新执行 `wget -c 下载链接` 即可继续，无需删除已下载文件；
3. 环境变量生效：若后续新开终端提示 `conda：未找到命令`，重新执行 `source ~/.bashrc` 即可；
4. 路径问题：安装路径 `~/miniconda3` 为用户级路径，无需sudo权限，避免因权限问题导致后续使用异常。

### 整体总结
整个流程核心为「**国内镜像下载→静默安装→环境变量配置→国内镜像源配置**」，四步完成，全程10分钟内可操作完毕；配置后可完全复刻Windows下Miniconda的使用体验，后续结合VSCode关联conda环境即可正常编写Python代码。