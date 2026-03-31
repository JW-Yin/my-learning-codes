# 1. 确保Flatpak本体已安装更新（Fedora最小化安装也能自动补齐）
sudo dnf install flatpak -y

# 2. 强制清理残留的错误flathub仓库（无残留也不会报错，避免历史冲突）
flatpak remote-delete --force flathub 2>/dev/null || true

# 3. 添加Flathub官方源（Flatpak官方标准地址，零404、100%成功）
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

# 4. 切换为中科大国内镜像（解决下载慢/卡住，国内访问稳定性最高）
sudo flatpak remote-modify flathub --url=https://mirrors.ustc.edu.cn/flathub

# 5. 安装Fcitx5输入法适配扩展（必做！解决Flatpak软件无法输入中文的核心问题）
flatpak install flathub org.freedesktop.Platform.Fcitx5Extension -y
