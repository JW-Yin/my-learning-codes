# 安装包管理工具（二选一）
- sudo apt install plasma-discover
- sudo apt install synaptic

# 安装从官网下载的.deb包
- 从u盘或官网找到所有需要的.deb包，依次执行sudo apt install 软件名.deb


# 安装apt-fast（加速下载且避免锁冲突）
sudo add-apt-repository ppa:apt-fast/stable
sudo apt update
sudo apt install apt-fast  
    - 以后用apt-fast代替apt，如`apt-fast install vlc`



