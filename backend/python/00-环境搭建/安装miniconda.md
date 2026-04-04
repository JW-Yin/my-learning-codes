# 🚀 Fedora 43 KDE 专属 | Miniconda 从零到 Py39 完整一键流程

# 安装
```bash
# 1. 安装依赖
sudo dnf install -y wget bzip2

# 2. 下载 Miniconda
cd ~/下载
wget -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 3. 静默安装
bash Miniconda3-latest-Linux-x86_64.sh -b -p ~/miniconda3

# 4. 配置环境变量
echo ". ~/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc
source ~/.bashrc

# 5. 删除冲突文件（解决 ToS 报错）
rm -f ~/miniconda3/.condarc

# 6. 配置 conda 清华源
conda config --remove-key channels
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch
conda config --set show_channel_urls yes

# 7. 关闭自动激活 base
conda config --set auto_activate_base false

# 8. 配置 pip 清华源
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF

# 9. 创建 Python 3.9 环境
conda create -n py39 python=3.9 -y

# 10. 激活并测试
conda activate py39
python --version
pip --version

```

# 完全移除
```bash
conda deactivate
rm -rf ~/miniconda3
sed -i '/conda.sh/d' ~/.bashrc
rm -rf ~/.condarc ~/.conda ~/.pip
source ~/.bashrc
```