# 一句话终极总结（最准）

- 要快速起很多实例、要弹性扩缩容、要环境统一 → 用 Docker
- 就单机稳稳跑、不用扩很多实例、追求极致性能 → 直接装在 宿主机 / 裸机

# Docker 零基础入门（从核心概念到实战，一步到位）
Docker 核心是「把应用和依赖打包成标准化容器」，让应用在任何机器上都能**环境一致、一键运行**——你可以把它理解成「应用的集装箱」，不管是Windows/Linux/Mac，集装箱里的应用运行环境完全一样，再也不用愁「在我机器上能跑，到你这就不行」。

---

## 一、先搞懂 3 个核心概念（新手必记）
用「外卖」做比喻，秒懂：
| 概念       | 通俗解释                | 类比                  |
|------------|-------------------------|-----------------------|
| 镜像（Image） | 应用的「安装包/模板」，包含代码、依赖、配置 | 外卖套餐的「菜单/模板」 |
| 容器（Container） | 镜像运行起来的「实例」，是独立的运行环境 | 按模板做好的「一份外卖」 |
| 仓库（Repository） | 存储镜像的「仓库」，类似代码仓库Git | 外卖平台（美团/饿了么） |

- 镜像：只读的，不能修改，是容器的「母版」；
- 容器：镜像的运行态，可启动/停止/删除，多个容器可基于同一个镜像创建；
- 仓库：最常用的是 Docker Hub（官方公共仓库），也有私有仓库（公司内部用）。

---

## 二、第一步：安装 Docker（以 Ubuntu 为例，最常用）
### 1. 卸载旧版本（如果有）
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

### 2. 安装依赖
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
```

### 3. 添加 Docker 官方 GPG 密钥
```bash
sudo install -m 0755 -d /etc/apt/trusted.gpg.d
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker.gpg
sudo chmod a+r /etc/apt/trusted.gpg.d/docker.gpg
```

### 4. 设置仓库
```bash
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/trusted.gpg.d/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 5. 安装 Docker 引擎
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 6. 验证安装成功
```bash
# 查看 Docker 版本
docker --version

# 运行官方测试容器（会自动拉取 hello-world 镜像）
sudo docker run hello-world
```
如果看到「Hello from Docker!」的输出，说明安装成功！

### （可选）免 sudo 使用 Docker
默认操作 Docker 需要 sudo，添加权限：
```bash
sudo usermod -aG docker $USER
# 重启终端或重新登录生效
```

---

## 三、第二步：核心命令实操（新手先掌握这 10 个）
从「跑一个 Nginx 容器」开始，手把手教：

### 1. 拉取镜像（从 Docker Hub 下载 Nginx 镜像）
```bash
docker pull nginx:latest  # latest 是版本标签，也可以指定版本如 nginx:1.25
```
- 执行后会显示镜像下载进度，完成后镜像就保存在本地了。

### 2. 查看本地镜像
```bash
docker images
# 或简写
docker image ls
```
输出示例：
```
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nginx        latest    0e901e68141f   2 hours ago    187MB
hello-world  latest    9c7a54a9a43c   2 months ago   13.3kB
```

### 3. 启动容器（运行 Nginx 容器）
```bash
# 核心命令：docker run [参数] 镜像名
# -d：后台运行；-p：端口映射（宿主机8080端口 → 容器80端口）；--name：给容器起名字
docker run -d -p 8080:80 --name my-nginx nginx:latest
```
- 解释：宿主机访问 `http://localhost:8080`，就能看到 Nginx 默认页面（容器里的 Nginx 跑在 80 端口，映射到宿主机 8080）。

### 4. 查看运行中的容器
```bash
docker ps
# 查看所有容器（包括停止的）
docker ps -a
```
输出示例：
```
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                  NAMES
a1b2c3d4e5f6   nginx:latest   "/docker-entrypoint.…"   10 seconds ago  Up 9 seconds   0.0.0.0:8080->80/tcp   my-nginx
```

### 5. 访问容器（验证 Nginx 运行）
```bash
curl http://localhost:8080
```
会返回 Nginx 的默认 HTML 页面，说明容器运行正常。

### 6. 进入容器（查看容器内部）
```bash
# docker exec -it 容器名/容器ID /bin/bash
docker exec -it my-nginx /bin/bash
```
- `-it`：交互式终端；执行后会进入容器的命令行，比如输入 `ls /usr/share/nginx/html` 能看到 Nginx 的静态文件。
- 退出容器：输入 `exit` 即可。

### 7. 停止容器
```bash
docker stop my-nginx
# 或用容器ID
docker stop a1b2c3d4e5f6
```

### 8. 启动已停止的容器
```bash
docker start my-nginx
```

### 9. 删除容器（必须先停止，否则加 -f 强制删除）
```bash
# 停止并删除
docker stop my-nginx && docker rm my-nginx
# 强制删除运行中的容器（谨慎用）
docker rm -f my-nginx
```

### 10. 删除镜像（先删除基于该镜像的所有容器）
```bash
docker rmi nginx:latest
# 强制删除（谨慎）
docker rmi -f nginx:latest
```

---

## 四、第三步：容器数据持久化（解决「容器删了数据丢」的问题）
容器默认是「临时的」，删除后里面的数据会丢失（比如 Nginx 的配置/静态文件），需要用「卷（Volume）」挂载数据：

### 示例：挂载本地目录到 Nginx 容器
```bash
# 1. 本地创建目录
mkdir -p ~/nginx/html ~/nginx/conf

# 2. 把容器里的默认配置复制到本地（方便修改）
docker cp my-nginx:/etc/nginx/nginx.conf ~/nginx/conf/

# 3. 重新启动容器，挂载本地目录
docker run -d -p 8080:80 \
  --name my-nginx \
  -v ~/nginx/html:/usr/share/nginx/html \  # 静态文件挂载
  -v ~/nginx/conf/nginx.conf:/etc/nginx/nginx.conf \  # 配置文件挂载
  nginx:latest
```
- `-v`：挂载卷，格式 `本地路径:容器内路径`；
- 现在修改本地 `~/nginx/html/index.html`，访问 `localhost:8080` 就能看到修改后的内容，容器删除后本地数据还在。

---

## 五、第四步：自定义镜像（写第一个 Dockerfile）
如果官方镜像不满足需求（比如要自定义 Nginx 页面），可以写 `Dockerfile` 构建自己的镜像：

### 1. 创建 Dockerfile 文件
```bash
mkdir my-nginx && cd my-nginx
touch Dockerfile
```

### 2. 写入以下内容（注释解释每一步）
```dockerfile
# 基础镜像（基于官方 Nginx）
FROM nginx:latest

# 作者信息（可选）
MAINTAINER yourname <your@email.com>

# 把本地的 index.html 复制到容器的 Nginx 静态目录
COPY index.html /usr/share/nginx/html/

# 暴露端口（只是声明，实际运行还是要 -p 映射）
EXPOSE 80
```

### 3. 创建自定义 index.html
```bash
echo "<h1>My Custom Nginx from Docker!</h1>" > index.html
```

### 4. 构建镜像（注意最后有个点，表示 Dockerfile 在当前目录）
```bash
docker build -t my-custom-nginx:v1 .
```
- `-t`：给镜像打标签，格式 `镜像名:版本`；
- 构建完成后，用 `docker images` 能看到 `my-custom-nginx:v1` 镜像。

### 5. 运行自定义镜像
```bash
docker run -d -p 8081:80 --name my-custom-nginx my-custom-nginx:v1
```
访问 `http://localhost:8081`，就能看到自定义的页面！

---

## 总结
1. Docker 核心是「镜像（模板）+ 容器（实例）」，解决环境不一致问题；
2. 新手先掌握：`pull`（拉镜像）→ `run`（启动容器）→ `ps`（看容器）→ `stop/rm`（停止/删容器）；
3. 数据持久化用 `-v` 挂载卷，自定义镜像用 `Dockerfile` 构建；
4. 容器适合部署无状态、需快速扩缩容的服务（如 Nginx、微服务），核心数据库可根据性能需求选择裸机/容器。
