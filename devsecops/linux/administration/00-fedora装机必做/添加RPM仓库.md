# Fedora 重装系统「RPM Fusion 全流程标准化配置指南」
**适配所有 Fedora 版本（43+）、KDE/GNOME 通用，零冲突、零报错，重装后直接照着抄即可一步到位**

---

## 一、核心流程总览（按顺序执行，一步不能乱）
```
1. 系统前置更新 → 2. 启用官方 openh264 仓库 → 3. 启用 RPM Fusion 双仓库 → 4. 国内镜像加速（可选）→ 5. 刷新缓存验证 → 6. 安装全功能音视频解码器 → 7. 验证成功
```

---

## 二、分步详解版（每步带作用说明，新手零出错）
### 步骤 1：系统前置更新（必做，避免依赖冲突）
重装系统后先执行，把所有预装包更新到最新，杜绝后续安装出现版本不匹配问题
```bash
sudo dnf update -y
```

### 步骤 2：启用官方配套 openh264 仓库（Fedora 41+ 必做）
解决浏览器、播放器的 H264 视频解码问题，和 RPM Fusion 完美配套
```bash
sudo dnf config-manager setopt fedora-cisco-openh264.enabled=1
```

### 步骤 3：一键启用 RPM Fusion free + nonfree 双仓库（核心）
**自动适配你当前的 Fedora 版本，不用手动改版本号，永久通用**
```bash
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm -y
```
- 说明：安装过程中提示「确认 GPG 密钥」，输入 `y` 回车即可
- `free` 仓库：开源自由软件；`nonfree` 仓库：闭源专有软件（如 NVIDIA 驱动、Steam）

### 步骤 4：国内镜像加速（可选，国内用户必加，下载速度提升10倍）
一键切换为清华大学开源镜像站，自动备份原配置，出问题可随时恢复
```bash
sudo sed -e 's|^mirrorlist=|#mirrorlist=|g' \
         -e 's|^#baseurl=http://download1.rpmfusion.org|baseurl=https://mirrors.tuna.tsinghua.edu.cn/rpmfusion|g' \
         -i.bak \
         /etc/yum.repos.d/rpmfusion-*.repo
```

### 步骤 5：刷新仓库缓存，验证仓库启用成功
```bash
# 刷新所有仓库缓存
sudo dnf makecache
# 验证仓库是否正常启用
dnf repolist | grep rpmfusion
```
✅ 成功标准：终端输出以下4行内容
```
rpmfusion-free                  RPM Fusion for Fedora XX - Free
rpmfusion-free-updates          RPM Fusion for Fedora XX - Free - Updates
rpmfusion-nonfree               RPM Fusion for Fedora XX - Nonfree
rpmfusion-nonfree-updates       RPM Fusion for Fedora XX - Nonfree - Updates
```

### 步骤 6：安装完整版 ffmpeg + 全格式音视频解码器（终极目标）
**自带冲突解决参数，直接规避预装 `ffmpeg-free` 阉割版的冲突问题，不会再出现报错**
```bash
sudo dnf install ffmpeg gstreamer1-plugins-{bad-\*,good-\*,base} gstreamer1-plugin-openh264 gstreamer1-libav --exclude=gstreamer1-plugins-bad-free-devel -y --allowerasing
```
- 作用：自动删除系统预装的阉割版 `ffmpeg-free`，替换为 RPM Fusion 全功能完整版 ffmpeg，一次性装完所有音视频解码插件，解决所有格式无法播放的问题

### 步骤 7：验证安装成功
```bash
ffmpeg -version
```
✅ 成功标准：输出内容中包含 `--enable-gpl` `--enable-nonfree` 字样，说明全功能版 ffmpeg 已安装完成。

---

## 三、重装系统极速版：一键执行脚本
**重装后直接复制整段到终端，回车输密码，全程自动完成所有配置，无需手动干预**
```bash
# 1. 系统更新
sudo dnf update -y
# 2. 启用openh264仓库
sudo dnf config-manager setopt fedora-cisco-openh264.enabled=1
# 3. 启用RPM Fusion双仓库
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm -y
# 4. 清华镜像加速
sudo sed -e 's|^mirrorlist=|#mirrorlist=|g' -e 's|^#baseurl=http://download1.rpmfusion.org|baseurl=https://mirrors.tuna.tsinghua.edu.cn/rpmfusion|g' -i.bak /etc/yum.repos.d/rpmfusion-*.repo
# 5. 刷新缓存
sudo dnf makecache
# 6. 安装全功能解码器
sudo dnf install ffmpeg gstreamer1-plugins-{bad-\*,good-\*,base} gstreamer1-plugin-openh264 gstreamer1-libav --exclude=gstreamer1-plugins-bad-free-devel -y --allowerasing
# 7. 验证安装结果
ffmpeg -version
```

---

## 四、启用仓库后，常用软件一键安装命令
装完 RPM Fusion 后，这些官方仓库没有的软件，直接一条命令搞定
| 软件/功能 | 安装命令 |
| :--- | :--- |
| NVIDIA 闭源显卡驱动 | `sudo dnf install akmod-nvidia -y` |
| Google Chrome 浏览器 | `sudo dnf install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm -y` |
| Steam 游戏平台 | `sudo dnf install steam -y` |
| VLC 全格式播放器 | `sudo dnf install vlc -y` |
| OBS 录屏直播软件 | `sudo dnf install obs-studio -y` |

---

## 五、核心避坑指南（新手必看，杜绝系统出问题）
1.  **不要用 `rpm -ivh 包名.rpm` 安装本地 rpm 包**：该命令不会自动解决依赖，极易搞崩系统；正确用法是 `sudo dnf install ./包名.rpm`
2.  **不要强制卸载 `ibus*` 通配符**：会删除 KDE 桌面依赖的底层库，直接导致桌面崩溃，仅卸载主程序即可
3.  **只添加信任的第三方仓库**：不明来源的仓库会导致系统依赖混乱，和 Ubuntu 乱加 PPA 同理
4.  **不要同时给 IBus 和 Fcitx5 设置环境变量**：会直接导致输入法冲突、弹窗报错
5.  **系统大版本升级前，先禁用第三方仓库**：避免升级过程中出现依赖冲突
