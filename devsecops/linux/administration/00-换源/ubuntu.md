```bash
# 备份
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
# 写入中科大源
sudo tee /etc/apt/sources.list > /dev/null << 'EOF'
deb https://mirrors.ustc.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
EOF
# 更新
sudo apt update
```