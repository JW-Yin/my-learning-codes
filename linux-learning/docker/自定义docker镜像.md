# 自定义 Docker 镜像完整流程
## 一、核心逻辑总览（先看大图）
1. **准备环境**：建一个干净的目录，放 Dockerfile 和自定义文件；
2. **定义镜像**：写 `Dockerfile`，告诉 Docker“我的镜像长什么样”；
3. **准备素材**：把要放进镜像的文件（比如 `index.html`）放在 Dockerfile 同级目录；
4. **构建镜像**：用 `docker build` 命令，基于 Dockerfile 生成专属镜像；
5. **验证镜像**：启动容器，确认镜像里的内容符合预期；
6. **（可选）版本管理**：通过升级标签（v1→v2）保留旧版本；
7. **（可选）清理**：删除无标签镜像，释放空间。

---

## 二、分步复盘（带命令+解释）
### 步骤 1：准备构建环境（建一个干净的目录）
**目的**：隔离构建上下文，避免无关文件干扰。
**命令**：
```bash
mkdir -p ~/my-docker  # 创建构建目录
cd ~/my-docker         # 进入该目录
```

---

### 步骤 2：写 Dockerfile（核心：定义镜像内容）
**目的**：告诉 Docker“我的镜像基于什么、要加什么文件、暴露什么端口”。
**命令**：
```bash
touch Dockerfile  # 新建 Dockerfile（注意文件名必须是 Dockerfile，无后缀）
```
**写入内容**（以自定义 Nginx 为例）：
```dockerfile
# 1. 基础镜像：自动拉取官方 Nginx 作为底层（不用手动 docker pull）
FROM nginx:latest

# 2. 复制文件：从构建上下文（当前目录）复制 index.html 到镜像指定目录
COPY index.html /usr/share/nginx/html/

# 3. 暴露端口：声明容器会用 80 端口（只是标记，不实际映射）
EXPOSE 80
```
**核心解释**：
- `FROM`：镜像的“地基”，必须是第一条指令；
- `COPY`：唯一“把本地文件加入镜像”的指令（只有 COPY 的文件才会进镜像）；
- `EXPOSE`：只是给使用者看的“提示”，实际端口映射靠 `docker run -p`。

---

### 步骤 3：准备自定义文件（比如 index.html）
**目的**：提供要放进镜像的“素材”（比如你的网页）。
**命令**：
```bash
echo "<h1>我的自定义 Docker 镜像！</h1>" > index.html
```
**验证**：
```bash
ls  # 此时目录里有：Dockerfile、index.html
```

---

### 步骤 4：构建镜像（生成专属镜像）
**目的**：基于 Dockerfile 生成带标签的自定义镜像。
**命令**：
```bash
docker build -t my-nginx:v1 .
```
**核心参数解释**：
- `-t my-nginx:v1`：给镜像打标签，`my-nginx` 是镜像名，`v1` 是版本号（方便识别）；
- `.`：指定「构建上下文」为当前目录（Docker 只能从这个目录里取文件）。
**成功标志**：最后出现 `Successfully tagged my-nginx:v1`。

---

### 步骤 5：验证镜像（确保能用）
#### 5.1 查看构建好的镜像
```bash
docker images my-nginx  # 只看 my-nginx 相关镜像
```
**输出示例**：
```
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
my-nginx     v1        xxxxxxxxxx     10 seconds ago 187MB
```

#### 5.2 启动容器测试
```bash
docker run -d -p 8081:80 --name test-my-nginx my-nginx:v1
```
**参数解释**：
- `-d`：后台运行；
- `-p 8081:80`：宿主机 8081 端口映射到容器 80 端口；
- `--name test-my-nginx`：给容器起个好记的名字。

#### 5.3 验证服务
```bash
curl http://localhost:8081
```
**成功标志**：返回你写的 `<h1>我的自定义 Docker 镜像！</h1>`。

#### 5.4 清理测试容器（可选）
```bash
docker stop test-my-nginx && docker rm test-my-nginx
```

---

### 步骤 6：（可选）版本管理（保留旧版本）
**目的**：避免覆盖旧镜像，方便回滚。
**做法**：升级版本号重新构建（不要重复用同一个标签）：
```bash
# 修改 index.html（比如加一行字）
echo "<h1>我的自定义 Docker 镜像！V2版本</h1>" > index.html

# 构建 v2 版本
docker build -t my-nginx:v2 .
```
**查看版本**：
```bash
docker images my-nginx
```
**输出**：
```
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
my-nginx     v2        yyyyyyyyyy     5 seconds ago  187MB
my-nginx     v1        xxxxxxxxxx     10 minutes ago 187MB
```
→ v1 和 v2 同时存在，想回滚直接用 `my-nginx:v1` 启动容器即可。

---

### 步骤 7：（可选）清理无标签镜像（释放空间）
**背景**：如果重复用同一个标签构建，旧镜像会变成 `<none>:<none>`（无标签镜像），占磁盘空间。
**命令**：
```bash
# 1. 查看无标签镜像
docker images -f dangling=true

# 2. 清理无标签镜像（安全）
docker image prune
```

---

## 三、复盘核心关键点（必记）
1. **Dockerfile 是“图纸”，镜像是“模板”，容器是“实例”**：
   - Dockerfile → 造镜像 → 启动容器；
2. **只有 COPY/ADD 的文件才会进镜像**：
   - 构建上下文里的其他文件只是“可供访问”，不会被打包；
3. **标签（-t）很重要**：
   - 格式：`镜像名:版本号`（推荐用 v1/v2/v3 区分版本）；
4. **`.` 是构建上下文**：
   - Docker 只能从这个目录里取文件，不能取目录外的文件；
5. **FROM 自动拉取基础镜像**：
   - 不用手动 `docker pull`，Docker 会自动处理。

---

## 四、快速回顾命令清单（复盘时直接看）
| 动作                | 命令                                  |
|---------------------|---------------------------------------|
| 建构建目录          | `mkdir -p ~/my-docker && cd ~/my-docker` |
| 写 Dockerfile       | `touch Dockerfile`（然后编辑内容）    |
| 构建镜像            | `docker build -t 镜像名:版本 .`       |
| 查看镜像            | `docker images 镜像名`                 |
| 启动容器测试        | `docker run -d -p 宿主机端口:容器端口 --name 容器名 镜像名:版本` |
| 验证服务            | `curl http://localhost:宿主机端口`     |
| 清理无标签镜像      | `docker image prune`                   |

---
