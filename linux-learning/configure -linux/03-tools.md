## 安装 GIMP
sudo apt install gimp -y

# 安装 VLC（自动处理依赖）
sudo apt install vlc -y

# 安装所有视频可以正常播放
sudo apt install ubuntu-restricted-extras

# 安装显示优化（浏览器按alt+F2，输入r；进入extensions.gnome.org搜索Dash to dock进行安装）
sudo apt install gnome-browser-connector

# 安装包管理
sudo apt install synaptic

# 安装apt-fast（加速下载且避免锁冲突）
sudo add-apt-repository ppa:apt-fast/stable
sudo apt update
sudo apt install apt-fast  
    - 以后用apt-fast代替apt，如`apt-fast install vlc`


