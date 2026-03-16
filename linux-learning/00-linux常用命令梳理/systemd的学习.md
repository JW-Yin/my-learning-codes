# systemd 系统学习指南
本文从基础认知到实战落地，循序渐进讲解systemd核心能力，覆盖日常运维90%以上的使用场景，新手可直接跟着操作。

---

## 一、基础认知：什么是systemd
`systemd` 全称 **system daemon**，是Linux系统的**系统与服务管理器**，PID=1的核心进程，是所有用户进程的祖先进程。
- 它替代了传统的SysVinit、Upstart，已成为RHEL/CentOS 7+、Ubuntu 16.04+、Debian 8+等主流发行版的默认init系统。
- 核心优势：并行启动服务大幅提升开机速度；统一管理服务、设备、挂载点、定时任务等所有系统资源；强大的依赖管理、进程监控、日志一体化能力。

### 核心概念：单元（Unit）
systemd将所有系统资源抽象为**单元**，每个单元对应一个配置文件，是systemd管理的最小单位。

常用单元类型（重点掌握前2个）：
| 单元后缀 | 核心用途 |
|---------|----------|
| `.service` | 系统服务管理，最常用，比如`sshd.service`、`nginx.service` |
| `.target` | 系统运行目标，用于分组管理多个单元，替代传统的运行级别 |
| `.socket` | 进程间通信套接字，实现服务按需启动 |
| `.mount` | 文件系统挂载点管理 |
| `.timer` | 定时任务，替代传统crontab |
| `.swap` | 交换分区/文件管理 |

---

## 二、核心工具：systemctl 常用命令（必背）
`systemctl` 是systemd的核心管理工具，日常90%的操作都围绕它展开，按场景分类整理如下：

### 1. 服务生命周期管理（.service专属）
| 命令 | 核心作用 |
|------|----------|
| `systemctl start 服务名` | 启动服务（`.service`后缀可省略，下同） |
| `systemctl stop 服务名` | 停止服务 |
| `systemctl restart 服务名` | 重启服务（服务未运行则直接启动） |
| `systemctl reload 服务名` | 重载服务配置（不重启进程，仅支持reload的服务，如nginx） |
| `systemctl status 服务名` | 查看服务详细状态、运行日志、PID、开机自启状态（排错核心命令） |

### 2. 开机自启管理
| 命令 | 核心作用 |
|------|----------|
| `systemctl enable 服务名` | 设置服务开机自启 |
| `systemctl enable --now 服务名` | 设置开机自启 + 立即启动服务（一步到位，高频使用） |
| `systemctl disable 服务名` | 禁用服务开机自启 |
| `systemctl disable --now 服务名` | 禁用开机自启 + 立即停止服务 |
| `systemctl is-enabled 服务名` | 查看服务是否开启开机自启 |
| `systemctl mask 服务名` | 彻底屏蔽服务（禁止任何方式启动，比disable更严格） |
| `systemctl unmask 服务名` | 取消服务屏蔽 |

### 3. 系统状态与单元查询
| 命令 | 核心作用 |
|------|----------|
| `systemctl list-units --failed` | 列出所有启动失败的单元（故障排错必用） |
| `systemctl list-unit-files --type=service --state=enabled` | 查看所有已开启开机自启的服务 |
| `systemctl cat 服务名` | 查看服务单元文件的完整内容（无需手动找路径） |
| `systemctl list-dependencies 服务名` | 查看服务的依赖树 |
| `systemctl daemon-reload` | 重载所有systemd单元配置（**修改/新增单元文件后必须执行**，否则配置不生效） |

### 4. 运行目标（Target）管理
| 命令 | 核心作用 |
|------|----------|
| `systemctl get-default` | 查看系统默认启动的Target |
| `systemctl set-default multi-user.target` | 设置默认启动为多用户字符界面（服务器推荐，关闭图形界面节省资源） |
| `systemctl isolate rescue.target` | 临时切换到单用户救援模式（系统故障排错用） |

### 5. 系统电源管理
| 命令 | 核心作用 |
|------|----------|
| `systemctl poweroff` | 关机 |
| `systemctl reboot` | 重启 |
| `systemctl suspend` | 挂起系统 |

---

## 三、核心进阶：服务单元文件详解
学会编写自定义服务单元文件，才算真正掌握systemd的核心能力。

### 1. 单元文件存放路径（优先级从高到低）
| 路径 | 用途 |
|------|------|
| `/etc/systemd/system/` | 管理员自定义的单元文件，优先级最高，会覆盖其他路径的同名文件 |
| `/run/systemd/system/` | 运行时动态生成的单元文件，重启后丢失 |
| `/usr/lib/systemd/system/` | 发行版/软件自带的单元文件，**禁止直接修改**，软件升级会被覆盖，需修改请复制到`/etc/systemd/system/`下操作 |

### 2. 服务单元文件核心结构
`.service` 文件分为三个核心区块，标准结构如下（附带完整示例）：
```ini
# 示例：自定义Python服务 /etc/systemd/system/my_demo.service
[Unit]
Description=My Demo Python Service
After=network.target syslog.target
Wants=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/my_demo
ExecStart=/usr/bin/python3 /opt/my_demo/app.py
Restart=on-failure
RestartSec=5s
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=my_demo

[Install]
WantedBy=multi-user.target
```

#### （1）[Unit] 区块：通用配置与依赖管理
用于描述单元信息、启动顺序、依赖关系，所有单元类型通用。
- `Description`：单元的描述信息，`status`命令中会显示
- `After`：指定本单元必须在哪些单元启动后再启动，**仅控制启动顺序，不控制依赖**
- `Before`：与`After`相反，指定本单元必须在哪些单元之前启动
- `Wants`：**弱依赖（推荐使用）**，本单元启动时会尝试启动指定单元，若依赖单元启动失败/停止，不影响本单元运行
- `Requires`：强依赖，本单元启动时必须同时启动指定单元，若依赖单元启动失败/停止，本单元也会被停止
- `Conflicts`：冲突单元，指定单元运行时，本单元无法启动，反之亦然

#### （2）[Service] 区块：服务核心配置
服务专属配置，控制进程的启动、运行、重启逻辑，是核心中的核心。
- `Type`：服务启动类型，决定systemd如何判断服务启动成功
  - `simple`：默认值，`ExecStart`启动的进程就是主进程，systemd认为服务启动后立即就绪，适合前台运行的程序（Python/Node.js脚本等自定义服务首选）
  - `forking`：适用于传统后台守护进程，`ExecStart`启动的进程会fork出子进程作为主进程，父进程退出后systemd认为服务启动成功，如nginx、redis、mysql
  - `oneshot`：一次性服务，进程执行完就退出，适合开机执行一次的初始化任务，通常配合`RemainAfterExit=yes`使用
  - `notify`：与simple类似，但服务就绪后会向systemd发送通知，systemd收到通知后才认为启动成功，需程序支持systemd通知机制
- `ExecStart`：服务启动时执行的命令，**必须使用绝对路径**，不能用相对路径/别名
- `ExecStartPre/ExecStartPost`：`ExecStart`执行前后运行的命令，用于环境准备、配置检查
- `ExecStop`：服务停止时执行的命令，不写则默认给主进程发送SIGTERM信号
- `ExecReload`：服务重载配置时执行的命令
- `Restart`：服务重启策略，控制systemd在什么情况下重启服务
  - `no`：默认值，从不重启
  - `on-failure`：**生产环境首选**，仅当服务异常退出（非0退出码、被信号杀死、超时）时重启
  - `always`：无论什么原因退出都重启，包括正常退出
- `RestartSec`：重启间隔，默认100ms，建议设置5s，避免频繁重启
- `User/Group`：服务运行的用户和用户组，**生产环境禁止用root运行业务服务**，提升安全性
- `WorkingDirectory`：服务的工作目录，程序中的相对路径基于此目录
- `Environment`：设置环境变量，如`Environment="JAVA_HOME=/usr/lib/jvm/java-17-openjdk" "ENV=prod"`
- `LimitNOFILE`：进程最大打开文件数，替代传统ulimit配置，如`LimitNOFILE=65535`

#### （3）[Install] 区块：开机自启配置
仅在执行`systemctl enable/disable`时生效，控制服务的开机自启行为。
- `WantedBy`：核心配置，指定本服务被哪个Target“需要”，enable时会在对应Target的`.wants`目录下创建软链接，实现开机自启
  - 自定义服务绝大多数写 `WantedBy=multi-user.target`（服务器默认多用户模式，开机自动启动）
  - 图形界面服务写 `WantedBy=graphical.target`
- `RequiredBy`：与WantedBy类似，为强依赖，极少使用

---

## 四、日志管理：journalctl 核心用法
`systemd-journald` 是systemd自带的日志系统，统一收集系统和所有服务的日志，存储为二进制格式，用`journalctl`命令查询，功能远超传统syslog。

### 高频常用命令
| 命令 | 核心作用 |
|------|----------|
| `journalctl -u 服务名 -f` | 实时滚动查看指定服务的日志（服务排错必用） |
| `journalctl -u 服务名 --since "10 minutes ago"` | 查看指定服务最近10分钟的日志 |
| `journalctl -f` | 实时查看系统全量日志 |
| `journalctl -k` | 只查看内核日志（等同于dmesg） |
| `journalctl -p err` | 只查看错误级别及以上的日志 |
| `journalctl --since "2026-03-10 09:00:00" --until "2026-03-10 18:00:00"` | 查看指定时间段的日志 |
| `journalctl --disk-usage` | 查看日志占用的磁盘空间 |
| `journalctl --vacuum-time=30d` | 清理日志，仅保留最近30天的日志 |
| `journalctl --vacuum-size=1G` | 清理日志，仅保留最多1G的日志 |

### 日志持久化配置
默认情况下，journald日志存储在`/run/log/journal/`，重启后丢失，如需持久化保存：
1. 修改配置文件 `/etc/systemd/journald.conf`
2. 将 `Storage=auto` 改为 `Storage=persistent`
3. 重启服务生效：`systemctl restart systemd-journald`
4. 日志将自动持久化到`/var/log/journal/`目录，重启不会丢失

---

## 五、实战演练：编写并运行自定义服务
跟着以下步骤，从零完成一个自定义服务的部署、启动、自启全流程。

### 步骤1：准备测试程序
创建`/opt/my_test/app.py`测试脚本：
```python
import time
from datetime import datetime

while True:
    print(f"[{datetime.now()}] 我的测试服务正在运行...")
    time.sleep(3)
```

### 步骤2：创建服务单元文件
创建`/etc/systemd/system/my_test.service`：
```ini
[Unit]
Description=My Test Service
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/my_test
ExecStart=/usr/bin/python3 /opt/my_test/app.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### 步骤3：重载配置并启动服务
```bash
# 重载systemd配置，必须执行
systemctl daemon-reload

# 启动服务
systemctl start my_test.service

# 查看服务状态
systemctl status my_test.service
```

### 步骤4：查看日志与设置自启
```bash
# 实时查看服务日志
journalctl -u my_test.service -f

# 设置开机自启并立即启动
systemctl enable --now my_test.service
```

### 步骤5：停止与禁用服务
```bash
# 禁用开机自启并立即停止服务
systemctl disable --now my_test.service
```

---

## 六、新手避坑指南
1. **修改单元文件后必须执行`systemctl daemon-reload`**，否则systemd不会加载新配置，修改不生效。
2. `ExecStart`必须使用**绝对路径**，systemd启动服务时不会加载用户环境变量，无法识别相对路径/别名。
3. 优先使用`Wants`弱依赖，少用`Requires`强依赖，避免依赖服务异常导致自身服务被停止。
4. `After/Before`仅控制启动顺序，必须配合`Wants/Requires`才能实现完整的依赖控制。
5. 禁止直接修改`/usr/lib/systemd/system/`下的系统自带单元文件，升级软件会被覆盖，需修改请复制到`/etc/systemd/system/`下操作。
6. 生产环境禁止用root用户运行业务服务，通过`User/Group`指定普通用户运行，降低安全风险。
7. 重启策略优先使用`on-failure`，避免`always`导致正常退出的服务被反复重启。

---

## 七、进阶拓展内容（学完基础后深入）
1. **定时任务`.timer`单元**：替代crontab，支持更灵活的定时规则，与systemd深度集成，自带日志、依赖、资源限制能力。
2. **资源限制**：通过`CPUQuota`、`MemoryMax`、`IOReadBandwidthMax`等配置，限制服务的CPU、内存、IO资源，替代手动cgroup配置。
3. **服务模板**：通过`@`创建模板单元文件（如`my_service@.service`），快速启动多个服务实例，适合多实例部署。
4. **启动优化**：用`systemd-analyze`工具分析系统启动耗时，`systemd-analyze blame`查看服务启动耗时排序，`systemd-analyze critical-chain`查看启动关键路径，优化开机速度。
5. **套接字激活`.socket`单元**：实现服务按需启动，仅当有请求访问对应套接字时才启动服务，节省系统资源。

### 一句话核心定义
`.target` 是 systemd 的**目标单元**，本质是「**单元分组管理工具 + 系统状态同步锚点**」。
它和 `.service`/`.timer` 最大的区别是：**本身不运行任何进程、不执行具体任务**，核心作用是把一组关联的单元（.service、.socket、.mount、甚至其他.target）打包组织在一起，定义系统应该达到的某个运行状态，同时统一管控单元的启动顺序和依赖关系。

---

## 一、用你熟悉的概念做类比，一秒懂定位
你已经理解了前两个单元，我们用生活化的类比彻底区分三者：
| 单元类型 | 类比角色 | 核心职责 |
|---------|----------|----------|
| `.service` | 一线干活的员工 | 执行具体任务、运行实际进程，是真正做事的主体 |
| `.timer` | 定时闹钟 | 到点触发，叫醒对应的.service去干活 |
| `.target` | 部门/项目组 | 本身不干活，只负责把相关的员工/单元打包成组，定义「项目要达到的状态」，统一管理启动顺序、批量启停，同时作为全公司的「里程碑节点」 |

举个你实战中见过的例子：
你写自定义服务时，`[Install]` 区块写了 `WantedBy=multi-user.target`，本质就是「把我的这个服务，加入到 `multi-user.target` 这个项目组里」。当系统启动到「多用户字符界面」这个状态时，就会自动启动这个项目组里的所有服务。

---

## 二、.target 的3个核心核心功能（日常运维全场景覆盖）
### 1. 替代传统 SysVinit 的「运行级别（runlevel）」，定义系统的启动状态
这是 `.target` 最广为人知的用途。
传统 Linux 用 0-6 七个数字定义系统的运行级别（比如3是多用户字符界面、5是图形界面），systemd 用 `.target` 完全替代了这套机制，每个运行级别对应一个专属的目标单元，逻辑更清晰、扩展性更强。

**核心对应关系（必记）**：
| 传统runlevel | 对应systemd.target | 核心用途 |
|--------------|---------------------|----------|
| 0 | `poweroff.target` | 关机 |
| 1 | `rescue.target` | 单用户救援模式（系统故障排错用） |
| 3 | `multi-user.target` | 多用户字符界面（服务器默认，无图形） |
| 5 | `graphical.target` | 图形界面（桌面版默认，依赖multi-user.target） |
| 6 | `reboot.target` | 重启系统 |

你之前用过的命令：
- `systemctl get-default`：查看系统默认启动的target（默认启动到哪个状态）
- `systemctl set-default multi-user.target`：设置默认启动到字符界面，就是把系统默认的运行状态设为这个target
- `systemctl isolate graphical.target`：临时切换到图形界面，就是让系统立即切换到这个target定义的状态，启动/停止对应的所有单元

### 2. 作为系统启动的「同步锚点」，彻底解决依赖和启动顺序混乱问题
这是 `.target` 最核心的设计价值，也是你写服务时最常用的功能。

举个最典型的场景：
你的Python/Java服务依赖网络就绪才能启动，而网络就绪需要启动`sshd`、`NetworkManager`、`firewalld`、网卡配置等一堆服务。如果每个依赖网络的服务，都要在`After`里写一堆服务名，不仅麻烦，还容易漏写、错写，一旦网络服务改名，所有依赖的服务都要改。

而 `.target` 完美解决了这个问题：
我们把**所有和网络相关的服务，全部归到 `network.target` 这个组里**，约定：`network.target` 启动完成 = 系统网络相关的所有服务都已启动，网络环境已就绪。

这样一来，你的服务只需要写一行：
```ini
[Unit]
After=network.target
Wants=network.target
```
就代表「等网络环境完全就绪后，再启动我的服务」，不用关心底层到底有多少个网络相关的服务，极大简化了依赖管理。

类似的常用锚点target：
- `basic.target`：系统基础就绪里程碑，代表挂载、系统日志、udev设备管理等所有基础系统服务都已启动完成，几乎所有业务服务都默认依赖它
- `sysinit.target`：系统初始化里程碑，负责内核模块加载、文件系统挂载、系统环境设置等早期启动任务
- `network-online.target`：比`network.target`更严格，代表**网络真正连通、网卡拿到IP、可以上网**，需要严格等待网络通的服务可以用它

### 3. 批量管理一组单元，实现一键启停、统一管控
当你有多个关联的服务时，`.target` 可以帮你实现批量管理，不用一个个操作服务。

举个实战场景：
你部署了一套网站，包含前端服务`frontend.service`、后端API服务`backend.service`、缓存服务`redis.service`、数据库服务`mysql.service`，这4个服务需要一起启动、一起停止、一起设置开机自启。

用 `.target` 可以一键搞定：
1.  创建一个自定义目标单元 `/etc/systemd/system/my_website.target`
    ```ini
    [Unit]
    Description=My Website Full Stack Target
    # 依赖多用户基础环境
    Requires=multi-user.target
    # 等基础环境就绪后再启动
    After=multi-user.target
    # 允许用isolate切换到这个目标
    AllowIsolate=yes

    [Install]
    WantedBy=multi-user.target
    ```
2.  把4个服务的 `[Install]` 区块，全部改成 `WantedBy=my_website.target`
3.  执行 `systemctl daemon-reload` 重载配置
4.  执行 `systemctl enable --now frontend backend redis mysql`，把服务加入到这个target的管理组

之后你就可以：
- 一键启动整套网站：`systemctl start my_website.target`
- 一键停止整套网站：`systemctl stop my_website.target`
- 一键查看整套服务的状态：`systemctl list-dependencies my_website.target`

---

## 三、.target 单元文件的核心结构（和.service的关键区别）
`.target` 的配置文件非常简单，**它没有 `[Service]` 区块**——因为它不运行任何进程，不需要定义启动命令、重启策略等。

它只有两个核心区块：`[Unit]` 和 `[Install]`，和你熟悉的.service的对应区块完全通用。

### 标准示例（系统内置multi-user.target简化版）
```ini
[Unit]
Description=Multi-User System
Documentation=man:systemd.special(7)
# 强依赖基础系统目标，基础环境没起来，这个target也不能启动
Requires=basic.target
# 冲突：救援模式运行时，这个target不能运行
Conflicts=rescue.service rescue.target
# 启动顺序：等基础目标、救援服务都处理完，再进入这个target
After=basic.target rescue.service rescue.target
# 允许用systemctl isolate切换到这个目标
AllowIsolate=yes

[Install]
# 别名：default.target默认指向它
Alias=default.target
```

### 关键配置说明
1.  `AllowIsolate=yes`：核心配置，允许用 `systemctl isolate` 命令临时切换到这个target，只有系统核心的运行级别target才需要开启，自定义的分组target按需开启。
2.  依赖配置（`Requires`/`Wants`/`After`/`Before`）：和.service完全通用，用于定义target之间的依赖和启动顺序，比如`graphical.target` 会依赖 `multi-user.target`，必须等字符界面的所有服务都启动完，才会启动图形界面。
3.  `WantedBy`：和.service的逻辑一致，enable时会在对应target的`.wants`目录下创建软链接，实现开机自启。

---

## 四、新手必看的避坑误区
1.  **误区1：.target 是一种服务，会运行进程**
    错！.target 本身不执行任何程序、不创建任何进程，它只是一个「分组标签」和「状态锚点」，真正干活的是它包含的.service等单元。

2.  **误区2：`After=network.target` 代表网络一定能通**
    错！`network.target` 只代表「网络管理服务已经启动」，不代表网卡拿到了IP、能正常上网。如果你的服务必须等网络完全连通才能启动，应该用：
    ```ini
    After=network-online.target
    Wants=network-online.target
    ```

3.  **误区3：自定义target必须写很多复杂配置**
    错！如果只是用来批量管理一组服务，自定义target只需要最基础的Description、依赖和启动顺序配置即可，甚至可以极简到几行。

4.  **误区4：`WantedBy` 只能写在.service里**
    其实反过来也可以：你可以在.target的`[Unit]`区块里写`Wants=xxx.service`，效果完全一致，只是管理视角不同。前者是「服务主动加入target」，后者是「target主动包含服务」。