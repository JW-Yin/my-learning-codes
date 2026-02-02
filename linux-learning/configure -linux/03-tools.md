
## Ksnip截图工具
sudo apt update && sudo apt install ksnip

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

