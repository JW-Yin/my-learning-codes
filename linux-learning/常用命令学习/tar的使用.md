### 先搞懂：tar 到底是什么？
`tar` 本身的意思是 **tape archive**（磁带归档），最初是为磁带备份设计的，现在是 Linux 打包的「标配」。
- 核心能力：**先打包（把多个文件/文件夹合并成一个 .tar 文件），再可选压缩**
- 关键特点：系统原生自带，无需额外安装，所有 Linux 发行版（Ubuntu/CentOS/RedHat 等）都支持

---

## 一、tar 核心参数（必记，就 5 个）
`tar` 命令的参数分「核心操作」和「辅助选项」，先记最核心的 5 个，其他都是锦上添花：

| 参数 | 含义 | 必用/可选 |
|------|------|-----------|
| `-c` | create（创建新的归档文件） | 打包时必用 |
| `-x` | extract（解压归档文件） | 解压时必用 |
| `-v` | verbose（显示打包/解压的详细过程） | 可选（推荐加，能看到进度） |
| `-f` | file（指定归档文件的名字） | 必用（且必须放在参数最后） |
| `-z`/`-j`/`-J` | 指定压缩算法 | 可选（打包+压缩时用） |

> 小技巧：参数可以合并写（比如 `-czvf` = `-c -z -v -f`），这是 Linux 命令的通用习惯。

---

## 二、tar 最常用的 4 个实战场景（学会就够用）
### 场景 1：仅打包（不压缩）→ .tar 文件
适合临时合并文件，不需要压缩的场景：
```bash
# 格式：tar -cvf 输出文件名.tar 要打包的文件/文件夹
tar -cvf test.tar ./my_folder/  # 打包 my_folder 文件夹为 test.tar
tar -cvf docs.tar file1.txt file2.md ./docs/  # 打包多个文件/文件夹
```
- 执行后会输出：`./my_folder/`、`./my_folder/file.txt` 等，代表正在打包这些文件（`-v` 的作用）。

### 场景 2：打包+gzip 压缩（最常用）→ .tar.gz 文件
这是 Linux 日常使用频率最高的方式，平衡速度和压缩率：
```bash
# 格式：tar -czvf 输出文件名.tar.gz 要打包的文件/文件夹
tar -czvf test.tar.gz ./my_folder/
```
- `-z`：启用 gzip 压缩，生成 `.tar.gz`（也可简写为 `.tgz`）。
- 对比纯打包：文件体积会小 30%-60%，速度很快，服务器/日常备份首选。

### 场景 3：打包+xz 压缩（压缩率最高）→ .tar.xz 文件
适合追求最小体积（比如传大文件、长期归档），不怕耗点 CPU/时间：
```bash
# 格式：tar -cJvf 输出文件名.tar.xz 要打包的文件/文件夹
tar -cJvf test.tar.xz ./my_folder/
```
- `-J`：启用 xz 压缩（注意是大写 J），生成 `.tar.xz`。
- 对比 `.tar.gz`：体积再小 20%-30%，但打包/解压速度慢一倍左右。

### 场景 4：解压 tar 文件（通用方法）
解压的核心是 `-x` 参数，压缩格式对应 `-z`/`-j`/`-J` 即可：
```bash
# 1. 解压 .tar.gz（最常用）
tar -xzvf test.tar.gz

# 2. 解压 .tar.xz
tar -xJvf test.tar.xz

# 3. 解压到指定目录（加 -C 参数，大写 C）
tar -xzvf test.tar.gz -C /home/user/desktop/  # 解压到桌面
```
> 小提醒：解压 `.tar` 纯打包文件，去掉压缩参数即可：`tar -xvf test.tar`。

---

## 三、tar 进阶小技巧（大佬常用）
### 1. 查看压缩包内容（不解压）
想知道包里有什么文件，不用解压，加 `-t` 参数：
```bash
tar -tzvf test.tar.gz  # 查看 .tar.gz 里的文件列表
```

### 2. 排除指定文件/文件夹打包
比如打包时不想包含 `node_modules` 或日志文件：
```bash
# 排除单个文件夹
tar -czvf test.tar.gz ./my_folder/ --exclude=./my_folder/node_modules

# 排除多个文件（用多个 --exclude）
tar -czvf test.tar.gz ./my_folder/ --exclude=*.log --exclude=tmp/
```

### 3. 打包时保留文件权限（服务器必备）
Linux 下文件有权限属性，加 `-p` 参数可保留权限，备份服务器文件时一定要加：
```bash
tar -czvf backup.tar.gz /etc/ -p  # 备份 /etc 目录，保留权限
```

---

### 总结
1. `tar` 是 Linux 原生打包工具，核心参数：`-c`（打包）、`-x`（解压）、`-f`（指定文件名，必放最后）、`-v`（看进度）。
2. 日常首选 `tar -czvf 文件名.tar.gz 文件夹`（打包）和 `tar -xzvf 文件名.tar.gz`（解压），覆盖 90% 场景。
3. 追求最小体积用 `tar -cJvf 文件名.tar.xz`，解压到指定目录加 `-C 路径`。

