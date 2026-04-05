# 📝 Fedora 43 安装 Docker **终极极简速查版**
（另一台设备直接按这个顺序复制，**1分钟装完，零报错**）

## 一、核心原则（为什么这么做）
1. 先删冲突：`podman` 与 Docker 不能共存
2. 不用旧 `dnf` 参数：Fedora 43 已弃用 `--add-repo`
3. 必须用**国内源**：直连 Docker 官方会 SSL 失败

---

# 🔥 完整可复制步骤（按顺序执行）
## 1. 清理冲突软件（必做）
```bash
sudo dnf remove -y podman skopeo containers-common
```

## 2. 安装依赖（已装会自动跳过）
```bash
sudo dnf install -y dnf-plugins-core
```

## 3. 添加 **阿里云 Docker 源**（唯一稳的方式）
```bash
sudo curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/fedora/docker-ce.repo -o /etc/yum.repos.d/docker-ce.repo
```

## 4. 安装 Docker 全套（含 compose）
```bash
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 5. 启动 Docker + 开机自启
```bash
sudo systemctl enable --now docker
```

## 6. 免 sudo 运行 Docker（必配）
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## 7. 验证安装成功
```bash
docker run hello-world
```

---

# ✅ 可选：国内镜像加速（推荐加上，拉镜像更快）
```bash
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
          "https://docker.jw-yin.xyz",
          "https://docker.m.daocloud.io"
  ]
}
EOF
```
重载配置：
```bash
sudo systemctl daemon-reload && sudo systemctl restart docker
```

---

# 🚀 另一台 Fedora 43 快速部署：
**直接全选下面 7 条，依次粘贴回车即可**
```bash
sudo dnf remove -y podman skopeo containers-common
sudo dnf install -y dnf-plugins-core
sudo curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/fedora/docker-ce.repo -o /etc/yum.repos.d/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

---

# 🔍 关键检查点（装完看这 2 条就够）
1. `docker --version` → 显示版本
2. `docker run hello-world` → 输出欢迎信息
