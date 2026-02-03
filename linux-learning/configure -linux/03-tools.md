
## Flameshot截图工具

- 下载适配Ubuntu 24.04的deb包
wget https://github.com/flameshot-org/flameshot/releases/download/v13.3.0/flameshot-13.3.0-1.ubuntu-24.04.amd64.deb

- 安装并自动修复依赖
sudo apt install -f ./flameshot-13.3.0-1.ubuntu-24.04.amd64.deb

## 安装 GIMP

sudo apt install gimp -y


## 安装 Flatpak

sudo apt update && sudo apt install flatpak -y
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo


## 安装 wiliwili

这是Linux平台最受欢迎的B站客户端，功能全面、更新频繁，基于MPV播放器，性能优秀。
1. 安装Flatpak（如未安装）
    ```bash
    sudo apt update && sudo apt install flatpak -y
    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    ```
2. 安装wiliwili
    ```bash
    flatpak install flathub cn.xfangfang.wiliwili -y
    ```
3. 启动与卸载
    - 启动：应用菜单搜索“wiliwili”或执行 `flatpak run cn.xfangfang.wiliwili`
    - 卸载：`flatpak uninstall cn.xfangfang.wiliwili`

