# 🍷 Fedora 快速配置 Wine + 中文 Notepad 一键流程

## 1. 安装 Wine
```bash
sudo dnf install -y wine wine-core wine-desktop
```

## 2. 安装字体源 + 中文字体
```bash
sudo dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

sudo dnf install -y msttcore-fonts-installer wqy-microhei-fonts wqy-zenhei-fonts
```

## 3. 设置 Wine 中文编码
```bash
WINEPREFIX=~/.wine wine reg add "HKLM\System\CurrentControlSet\Control\Nls\CodePage" /v "ACP" /t REG_SZ /d "936" /f
WINEPREFIX=~/.wine wine reg add "HKLM\System\CurrentControlSet\Control\Nls\CodePage" /v "OEMCP" /t REG_SZ /d "936" /f
WINEPREFIX=~/.wine wine reg add "HKLM\System\CurrentControlSet\Control\Nls\Language" /v "InstallLanguage" /t REG_SZ /d "0804" /f
WINEPREFIX=~/.wine wine reg add "HKLM\System\CurrentControlSet\Control\Nls\Language" /v "Default" /t REG_SZ /d "0804" /f
```

## 4. 写入字体替换配置
```bash
cat <<EOF > ~/.wine/system.reg
[Software\\Microsoft\\Windows NT\\CurrentVersion\\FontSubstitutes] 16777217
"MS Shell Dlg"="WenQuanYi Micro Hei"
"MS Shell Dlg 2"="WenQuanYi Micro Hei"
"Tahoma"="WenQuanYi Micro Hei"
"SimSun"="WenQuanYi Micro Hei"
"Microsoft YaHei"="WenQuanYi Micro Hei"
EOF
```

## 5. 重启 Wine 生效
```bash
wineserver -k
wineboot -u
```

## 6. 测试 Notepad
```bash
wine notepad
```

---