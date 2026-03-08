## 一、先准备一个自定义脚本（作为被托管的服务）

我们先写一个简单的示例脚本，比如一个持续打印日志的服务脚本：

```bash
# 创建脚本文件
sudo vim /usr/local/bin/my_demo_service.sh
```

写入以下内容：
```bash
#!/bin/bash
while true; do
    echo "My custom service is running at $(date)"
    sleep 5
done
```

然后给脚本加上执行权限：
```bash
sudo chmod +x /usr/local/bin/my_demo_service.sh
```

> 这个脚本会每隔5秒打印一行日志，模拟一个持续运行的服务。

---

## 二、编写 .service 单元文件（核心步骤）

我们需要创建一个 `.service` 文件，告诉 systemd 如何管理我们的脚本。

```bash
# 创建单元文件
sudo vim /etc/systemd/system/my_demo_service.service
```

写入以下内容（我会逐段解释）：

```ini
[Unit]
Description=My Custom Demo Service
After=network.target  # 表示在网络服务启动后再启动本服务

[Service]
Type=simple          # 简单类型，ExecStart启动的进程就是服务主进程
ExecStart=/usr/local/bin/my_demo_service.sh  # 必须是脚本的绝对路径
Restart=always       # 重启策略：无论进程是正常退出还是异常退出，都自动重启
RestartSec=3         # 重启前等待3秒
User=root            # 以 root 用户运行（可按需改为普通用户）
StandardOutput=journal+console  # 把标准输出重定向到 systemd 日志

[Install]
WantedBy=multi-user.target  # 表示在多用户模式下启用开机自启
```

### 关键配置解释：
- **[Unit]**：定义服务的元信息和依赖关系。
  - `Description`：服务的描述，方便识别。
  - `After`：指定启动顺序，确保在依赖服务之后启动。
- **[Service]**：定义服务的执行规则和重启策略。
  - `Type=simple`：最常用的类型，适用于持续运行的脚本。
  - `ExecStart`：服务启动时执行的命令，必须是绝对路径。
  - `Restart=always`：确保服务意外退出后，systemd 会自动拉起。其他常用值：`on-failure`（仅在异常退出时重启）。
  - `RestartSec`：重启前的等待时间，避免频繁重启。
- **[Install]**：定义服务的安装信息，与开机自启相关。
  - `WantedBy=multi-user.target`：表示在系统进入多用户模式时启动本服务。

---

## 三、部署并加载配置，启动服务

1.  **重新加载 systemd 配置**（必须执行，让 systemd 识别新的单元文件）：
    ```bash
    sudo systemctl daemon-reload
    ```

2.  **启动服务**：
    ```bash
    sudo systemctl start my_demo_service.service
    ```

3.  **验证服务状态**：
    ```bash
    sudo systemctl status my_demo_service.service
    ```
    你应该看到类似这样的输出，表示服务正在运行：
    ```
    ● my_demo_service.service - My Custom Demo Service
         Loaded: loaded (/etc/systemd/system/my_demo_service.service; disabled; vendor preset: enabled)
         Active: active (running) since Mon 2024-03-07 10:00:00 CST; 5s ago
       Main PID: 12345 (my_demo_service.sh)
          Tasks: 2 (limit: 4915)
         Memory: 1.2M
            CPU: 10ms
         CGroup: /system.slice/my_demo_service.service
                 ├─12345 /bin/bash /usr/local/bin/my_demo_service.sh
                 └─12346 sleep 5
    ```

4.  **查看服务日志**（可选，用于排查问题）：
    ```bash
    sudo journalctl -u my_demo_service.service -f
    ```
    你会看到脚本每隔5秒打印的日志。

---

## 四、设置开机自启，重启验证

1.  **设置开机自启**：
    ```bash
    sudo systemctl enable my_demo_service.service
    ```
    输出会显示创建了一个软链接，将服务链接到 `multi-user.target` 的启动目录。

2.  **重启服务器**：
    ```bash
    sudo reboot
    ```

3.  **重启后验证**：
    服务器重启后，再次检查服务状态：
    ```bash
    sudo systemctl status my_demo_service.service
    ```
    如果服务状态为 `active (running)`，说明开机自启生效。

---

## 五、手动杀掉进程，验证自动拉起

1.  **找到服务的 PID**：
    ```bash
    ps aux | grep my_demo_service.sh
    ```
    输出中会显示服务的 PID，比如 `12345`。

2.  **手动杀掉进程**：
    ```bash
    sudo kill -9 12345
    ```

3.  **立即查看服务状态**：
    ```bash
    sudo systemctl status my_demo_service.service
    ```
    你会发现服务的 PID 已经变了，并且状态仍然是 `active (running)`。这说明 systemd 成功地自动拉起了服务。

---

## 六、作业验收清单

对照作业要求，逐一检查：

1.  ✅ 独立编写 .service 单元文件，配置了执行规则和重启策略。
2.  ✅ 部署了单元文件，执行了 `daemon-reload`，启动了服务并验证了状态。
3.  ✅ 设置了开机自启，重启服务器后验证了自启生效。
4.  ✅ 手动杀掉进程，验证了 systemd 能自动拉起服务。

---

## 常见问题排查

- **服务启动失败**：用 `journalctl -u my_demo_service.service` 查看日志，检查脚本路径是否正确、权限是否足够。
- **开机自启不生效**：确保 `WantedBy=multi-user.target` 配置正确，并且执行了 `enable` 命令。
- **自动拉起不生效**：检查 `Restart` 策略是否为 `always` 或 `on-failure`，并且服务类型 `Type=simple` 配置正确。

---
