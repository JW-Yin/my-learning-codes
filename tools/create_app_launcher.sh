#!/bin/bash
# ====================== 只需修改下面这部分配置 ======================
# 1. 启动器文件名（最终生成 xxx.desktop，比如 idea.desktop、goland.desktop）
APP_DESKTOP_NAME="idea.desktop"
# 2. 应用显示名称（菜单里看到的名字，比如 IntelliJ IDEA、GoLand）
APP_DISPLAY_NAME="IntelliJ IDEA"
# 3. 应用描述（可选，随便写）
APP_COMMENT="The Drive to Develop"
# 4. 应用执行路径（你手动运行的绝对路径，比如 /opt/idea/bin/idea）
APP_EXEC_PATH="/opt/idea/bin/idea"
# 5. 应用图标路径（svg/png/jpg 都可以，绝对路径）
APP_ICON_PATH="/opt/idea/bin/idea.svg"
# 6. 应用分类（决定在菜单哪个分类下，参考下面的「分类参考表」）
APP_CATEGORIES="Development;IDE;Java;"
# ====================== 下面的内容无需修改 ======================

# 生成 .desktop 文件
cat > ~/.local/share/applications/${APP_DESKTOP_NAME} << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=${APP_DISPLAY_NAME}
Comment=${APP_COMMENT}
Exec=${APP_EXEC_PATH}
Icon=${APP_ICON_PATH}
Terminal=false
Categories=${APP_CATEGORIES}
StartupWMClass=${APP_WM_CLASS}
StartupNotify=true
EOF

# 添加执行权限
chmod +x ~/.local/share/applications/${APP_DESKTOP_NAME}

# 刷新应用菜单
update-desktop-database ~/.local/share/applications/

# 提示完成
echo -e "\033[32m✅ 启动器创建成功！\033[0m"
echo -e "📌 应用名称：${APP_DISPLAY_NAME}"
echo -e "📂 启动器文件：~/.local/share/applications/${APP_DESKTOP_NAME}"
echo -e "💡 按 Super 键搜索「${APP_DISPLAY_NAME}」即可找到"
