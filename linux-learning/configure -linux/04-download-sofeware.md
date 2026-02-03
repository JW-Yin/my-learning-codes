# Linux 软件安装卸载+缓存清理梳理
## 一、各安装方式及对应卸载（普通→完全卸载）
按「系统原生→便携通用→跨发行版→Windows兼容→兜底编译」优先级整理，含每种方式的安装操作、普通卸载、完全卸载步骤：

### 1. APT（系统原生，首选）
#### 安装操作
- 搜索软件：`sudo apt search 软件名`
- 更新软件源（可选）：`sudo apt update`
- 安装软件：`sudo apt install 软件名 -y`
- 批量更新已装软件：`sudo apt upgrade`

#### 卸载操作
- 普通卸载（保留配置）：`sudo apt remove 软件名`
- 彻底卸载（删除配置）：`sudo apt purge 软件名`
- 清理残留依赖：`sudo apt autoremove`
- 手动清理用户配置（兜底）：`rm -rf ~/.config/软件名/`

### 2. GitHub/官网（APT无包时首选，分deb/AppImage）
#### 2.1 deb包（接近系统原生）
##### 安装操作
- 下载：官网/GitHub下载对应架构（amd64）deb包
- 图形化安装：双击deb包 → 软件中心点击「安装」
- 命令行安装：`sudo dpkg -i deb包文件名.deb`
- 修复依赖（安装失败时）：`sudo apt -f install`

##### 卸载操作（同APT）
- 普通卸载：`sudo apt remove 软件名`
- 彻底卸载：`sudo apt purge 软件名`
- 清理残留依赖：`sudo apt autoremove`
- 手动清理用户配置：`rm -rf ~/.config/软件名/`

#### 2.2 AppImage（便携免安装）
##### 安装/运行操作
- 下载：官网/GitHub下载对应架构AppImage包
- 赋予执行权限：`chmod +x AppImage文件名.AppImage`（或图形化勾选）
- 运行：`./AppImage文件名.AppImage`（或双击）

##### 卸载操作
- 普通卸载：直接删除AppImage文件
- 彻底卸载：删除AppImage文件 + 手动清理配置（`rm -rf ~/.config/软件名/`）

### 3. Flatpak/Snap（前两种无包时选，跨发行版）
#### 前置安装
- Flatpak：
  ```bash
  sudo apt install flatpak -y
  flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
  reboot  # 需重启生效
  ```
- Snap：`sudo apt install snapd -y`（Ubuntu默认预装，无需重启）

#### 3.1 Flatpak
##### 安装操作
- 搜索：`flatpak search 软件名`
- 安装：`flatpak install flathub 软件ID -y`
- 运行：`flatpak run 软件ID`

##### 卸载操作
- 普通卸载：`flatpak uninstall 软件ID -y`
- 彻底卸载：`flatpak uninstall --delete-data 软件ID -y`
- 清理无用运行时依赖：`flatpak uninstall --unused`

#### 3.2 Snap
##### 安装操作
- 搜索：`snap search 软件名`
- 安装：`sudo snap install 软件名`（部分需加`--classic`）
- 运行：直接输入软件名

##### 卸载操作
- 普通卸载：`sudo snap remove 软件名`
- 彻底卸载：`sudo snap remove --purge 软件名`
- 清理旧缓存：`sudo snap cleanup`

### 4. Deepin-Wine（Windows软件专属）
#### 安装操作
- 安装核心组件：
  ```bash
  git clone https://gitee.com/wszqkzqk/deepin-wine-for-ubuntu.git
  cd deepin-wine-for-ubuntu
  ./install.sh
  ```
- 安装软件：下载适配版deb包 → `sudo dpkg -i 软件名.deb`

#### 卸载操作
- 卸载单个软件（普通）：`sudo apt remove 软件名`（如`deepin-wechat`）
- 彻底卸载单个软件：`sudo apt purge 软件名 && sudo apt autoremove`
- 清理残留配置：`rm -rf ~/.deepinwine/软件名/`
- 卸载核心组件：进入`deepin-wine-for-ubuntu`目录 → `./uninstall.sh`

### 5. 源码编译（极端兜底，新手慎试）
#### 安装操作
```bash
# 1. 安装编译依赖
sudo apt install build-essential cmake make gcc g++ -y
# 2. 解压源码包（tar.gz为例）
tar -zxvf 源码包名.tar.gz
# 3. 配置参数
cd 源码目录名 && ./configure  # 部分用 cmake .
# 4. 编译（-j4 为4核加速，按需修改）
make -j4
# 5. 安装
sudo make install
```

#### 卸载操作
- 尝试卸载：`sudo make uninstall`（需在源码目录执行）
- 失败兜底：手动删除安装文件（易残留，不推荐新手）

## 二、缓存残留清理（完全卸载后仍需清理）
### 1. 缓存基础说明
- 缓存为“安装包/运行时备份”，不删不影响功能，仅占用磁盘空间；
- 不手动清理则不会自动消失（超旧缓存可能被工具自动清理）。

### 2. 各工具缓存清理命令
| 工具类型     | 缓存作用                  | 清理命令                          |
|--------------|---------------------------|-----------------------------------|
| APT          | 存储deb安装包（重装免下载） | 清理旧缓存：`sudo apt autoclean` <br> 清理所有缓存：`sudo apt clean` |
| Flatpak      | 存储安装包和运行时文件    | `flatpak uninstall --unused`      |
| Snap         | 存储安装包和缓存文件      | `sudo snap cleanup`               |
| AppImage     | 无安装缓存                | 无需清理                          |
| Deepin-Wine  | 依赖APT缓存               | 同APT清理命令（autoclean/clean）  |