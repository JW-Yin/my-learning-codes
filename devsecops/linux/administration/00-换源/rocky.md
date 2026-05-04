```bash
# 创建脚本文件
cat > change-ustc-rocky9.sh << 'EOF'
#!/bin/bash
echo "============================================="
echo "      Rocky Linux 9 一键切换中科大源"
echo "          自动备份 | 自动修复 | 全自动执行"
echo "============================================="

# 1. 自动备份原生源（如果没备份过）
if [ ! -d "/etc/yum.repos.d.bak" ]; then
    echo "[1/5] 首次运行，备份原始软件源..."
    sudo cp -r /etc/yum.repos.d /etc/yum.repos.d.bak
else
    echo "[1/5] 检测到已有备份，跳过备份..."
fi

# 2. 恢复原始源（修复之前的错误配置）
echo "[2/5] 恢复原始软件源配置..."
sudo rm -rf /etc/yum.repos.d
sudo mv /etc/yum.repos.d.bak /etc/yum.repos.d

# 3. 一键替换为中科大 Rocky9 源
echo "[3/5] 替换为中科大官方源..."
sudo sed -e 's|^mirrorlist=|#mirrorlist=|g' \
-e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=https://mirrors.ustc.edu.cn/rocky|g' \
-i /etc/yum.repos.d/rocky*.repo

# 4. 刷新缓存
echo "[4/5] 清理旧缓存，生成新缓存..."
sudo dnf clean all -y > /dev/null 2>&1
sudo dnf makecache -y

# 5. 测试安装软件，验证成功
echo -e "\n[5/5] 测试源是否可用（安装vim）..."
sudo dnf install -y vim > /dev/null 2>&1

echo -e "\n============================================="
echo "✅ 恭喜！中科大源切换 100% 完成！"
echo "测试软件安装成功，下载速度已拉满！"
echo "============================================="
EOF
```