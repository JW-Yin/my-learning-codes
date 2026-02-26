# gimp图像编辑工具（去plasma-discover中下载）  

# 安装完整的音乐解码库
```bash
sudo apt update && sudo apt install gstreamer1.0-plugins-good gstreamer1.0-plugins-ugly gstreamer1.0-libav ffmpeg
```

# Mark Text（markdown工具）
```bash
sudo apt update && sudo apt install -y libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6 xdg-utils libatspi2.0-0 libdrm2 libgbm1 libasound2

去官网找deb包：https://github.com/marktext/marktext/releases

sudo apt install -y ./marktext-amd64.deb

```

## VLC
```bash
sudo apt update && sudo apt install vlc -y
vlc --version
```

## 更换真正的firefox
更换前先去官网下载最新版的firefox
```bash
sudo snap remove --purge firefox
sudo rm -rf /var/snap/firefox
```