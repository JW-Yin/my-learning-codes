# 安装apt-fast（加速下载且避免锁冲突）
sudo add-apt-repository ppa:apt-fast/stable
sudo apt update
sudo apt install apt-fast  
    - 以后用apt-fast代替apt，如`apt-fast install vlc`

# 安装依赖自动管理工具 aptitude
`sudo apt-get install aptitude`
- 以后再安装任何东西都可以使用`sudo aptitude install <package_name>`，等价替换`sudo apt install <package_name>`

# 安装图形化包管理工具
1. `sudo apt upgrade -y`
2. `sudo apt install plasma-discover -y`

# 安装pig_cha
1. 去这里注册账号并且下载`.deb`包：`https://link.vtlovenet.xyz/register?share_id=5799cb22-c501-4fe2-8414-786e3b5aa3f2&lang=zh`
1. `sudo apt install libappindicator3-1 -y`
1. `sudo dpkg -i ViewTurboLite_amd64.deb`

# C语言开发环境
`sudo apt install build-essential -y`

# gimp图像编辑工具（去plasma-discover中下载）

# 安装完整的音乐解码库
```
sudo apt update && sudo apt install gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-libav ffmpeg
```