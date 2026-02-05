# 适配Ubuntu 22.04的Wine完整安装+基础配置流程

## 一、基础Wine/Winetricks安装
### Wine安装及初始化
```bash
sudo apt update && sudo apt install wine-stable -y
winecfg # 初始化生成Wine核心的模拟注册表、C盘目录等
```

### Winetricks安装
```bash
# 1. 卸载系统自带旧版Winetricks
sudo apt remove winetricks -y
# 2. 下载官方最新版Winetricks
wget https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks
# 3. 赋予文件可执行权限
chmod +x winetricks
# 4. 移动到系统全局目录，支持任意位置调用
sudo mv winetricks /usr/local/bin/
# 5. 创建软链接，解决终端路径检索优先级问题（核心修复）
sudo ln -s /usr/local/bin/winetricks /usr/bin/winetricks
# 6. 验证升级成功（显示2024/2025版即为成功）
winetricks --version
```

## 二、安装Wine必备核心依赖（解决程序运行/截屏报错）
基于你运行PixPin出现的`concrt140.dll缺失`「OLE组件未注册」等问题，安装**完整依赖包**并注册系统组件，确保绝大多数Windows程序正常运行，按顺序执行命令：
```bash
# 1. 安装完整VC++2019运行库（含并发库concrt140.dll，解决核心dll缺失）
winetricks vcrun2019-sp1
# 2. 安装wine-gecko（HTML渲染组件，适配微信/QQ/带网页界面的程序）
winetricks wine-gecko
# 3. 注册OLE核心组件（解决截屏/组件未注册报错，执行后显示「成功」即可）
cd ~/.wine/drive_c/windows/system32/ && wine regsvr32 ole32.dll && wine regsvr32 oleaut32.dll
```
💡 安装`vcrun2019-sp1`时弹出Windows安装向导，**所有选项默认**，直接点「下一步→安装→完成」，无需修改。


## 五、Wine环境验证：运行Windows .exe程序

### 终端命令运行
```bash
# 格式：wine 程序完整路径
wine ~/桌面/auto_script/PixPin_1.8.2.0/PixPin/PixPin.exe
```

