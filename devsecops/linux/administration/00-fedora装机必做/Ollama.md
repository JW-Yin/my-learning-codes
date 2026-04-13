# Fedora 43 重装后快速部署 Ollama + AMD ROCm + DeepSeek R1 流程
全程只需要按顺序复制命令，**10 分钟搞定**

---

## 0. 提前下载好两个文件（去 GitHub Releases）
- `ollama-linux-amd64.tar.zst`（主程序）
- `ollama-linux-amd64-rocm.tar.zst`（AMD 显卡加速库）
放到 `~/下载`

---

## 1. 解压文件
```bash
cd ~/下载

# 先解压主程序
tar -I zstd -xvf ollama-linux-amd64.tar.zst

# 再解压 ROCm 加速包（会自动补全 lib）
tar -I zstd -xvf ollama-linux-amd64-rocm.tar.zst
```

---

## 2. 安装到系统目录
```bash
sudo cp bin/ollama /usr/local/bin/
sudo chmod +x /usr/local/bin/ollama
sudo cp -r lib/ollama /usr/lib/
```

---

## 3. 安装 Fedora 显卡依赖
```bash
sudo dnf install -y mesa-libOpenCL clinfo
```

---

## 4. 创建 Ollama 系统服务（开机自启 + AMD 加速）
```bash
sudo tee /etc/systemd/system/ollama.service <<EOF
[Unit]
Description=Ollama
After=network.target

[Service]
Environment=LD_LIBRARY_PATH=/usr/lib/ollama/rocm:\$LD_LIBRARY_PATH
Environment=HIP_VISIBLE_DEVICES=0
Environment=OLLAMA_HOST=127.0.0.1
ExecStart=/usr/local/bin/ollama serve
User=$USER
Group=$USER
Restart=always

[Install]
WantedBy=default.target
EOF
```

---

## 5. 启动服务并设置开机自启
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ollama
```

检查状态：
```bash
sudo systemctl status ollama
```

---

## 6. 下载并运行模型
```bash
# 拉取 DeepSeek R1 14B
ollama pull deepseek-r1:14b

# 运行
ollama run deepseek-r1:14b
```

---

# 极简备忘版（重做系统直接照着敲）
```bash
cd ~/下载
tar -I zstd -xvf ollama-linux-amd64.tar.zst
tar -I zstd -xvf ollama-linux-amd64-rocm.tar.zst

sudo cp bin/ollama /usr/local/bin/
sudo chmod +x /usr/local/bin/ollama
sudo cp -r lib/ollama /usr/lib/

sudo dnf install -y mesa-libOpenCL clinfo

sudo tee /etc/systemd/system/ollama.service <<EOF
[Unit]
Description=Ollama
After=network.target
[Service]
Environment=LD_LIBRARY_PATH=/usr/lib/ollama/rocm:\$LD_LIBRARY_PATH
Environment=HIP_VISIBLE_DEVICES=0
Environment=OLLAMA_HOST=127.0.0.1
ExecStart=/usr/local/bin/ollama serve
User=$USER
Group=$USER
Restart=always
[Install]
WantedBy=default.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now ollama

ollama pull deepseek-r1:14b
ollama run deepseek-r1:14b
```