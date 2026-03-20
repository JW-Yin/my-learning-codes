
**适用场景**：解决国内环境Docker Hub镜像拉取超时、限流、速度慢问题；
**核心域名**：`<你自己的域名>`；
**绑定加速域名**：`<docker.你自己的域名>`；

---

## 一、方案核心原理

通过Cloudflare Worker实现Docker Hub反向代理，将自己的域名作为加速入口，借助Cloudflare全球节点完成镜像拉取的中转加速，全程国内可操作，无需额外工具，合规仅用于公开镜像加速。
- 核心链路：本地Docker → 自定义加速域名 → Cloudflare Worker → Docker Hub官方源 → 回源返回镜像数据
- 优势：零服务器成本、配置灵活、节点覆盖广、可规避Docker Hub原生限流

---

## 二、前置准备清单（必看）
| 准备项 | 要求 | 备注 |
|--------|------|------|
| 实名域名 | 国内/境外注册均可，无需备案 | 本次使用`<你自己的域名>`，阿里云注册 |
| Cloudflare账号 | 普通邮箱即可注册，免费计划完全够用 | 中文官网国内可直接访问：https://www.cloudflare.com/zh-cn/ |
| 本地环境 | 已安装Docker的Ubuntu系统 | 需有sudo权限，可修改Docker daemon配置 |

---

## 三、完整可复现落地步骤
### 阶段1：域名DNS解析权移交Cloudflare（核心前提，踩坑重灾区）
1.  登录域名注册商控制台（本次为阿里云），进入目标域名`<你自己的域名>`的**DNS修改/域名管理**页面
2.  删除原有的默认DNS服务器地址，完整粘贴Cloudflare分配的2个专属NS地址：
    ```
    crystal.ns.cloudflare.com
    gannon.ns.cloudflare.com
    ```
3.  保存修改，等待DNS生效（国内域名通常5-30分钟，最长不超过24小时）
4.  生效验证命令（Ubuntu终端执行）：
    ```bash
    dig NS <你自己的域名>
    ```
    ✅ 成功标准：返回结果仅包含Cloudflare的2个NS地址，无其他DNS服务器

### 阶段2：Cloudflare站点添加与激活

1.  Cloudflare控制台点击「添加站点」，输入域名`<你自己的域名>`，选择**免费Free计划**
2.  等待Cloudflare自动检测NS修改，站点首页显示**「您的域现在受Cloudflare保护」/ 站点活跃Active**，即激活成功
3.  无需手动添加任何DNS解析记录，后续绑定Worker时Cloudflare会自动生成

### 阶段3：基础链路验证（Hello World Worker，必做！先通基础再上业务）
#### 核心目的：提前验证「域名→Cloudflare Worker」链路是否正常，规避后续业务代码排查复杂度

1.  Cloudflare左侧菜单进入「Workers 和 Pages」，点击「创建应用程序→Worker→创建Worker」
2.  命名Worker（如`hello-world`），点击部署，使用Cloudflare默认的Hello World模板
3.  进入Worker详情页→「触发器」→「自定义域」→「添加自定义域」，输入二级域名`<docker.你自己的域名>`
4.  等待1分钟，自定义域状态变为**有效/Active**，Cloudflare自动生成DNS记录
5.  浏览器访问`https://<docker.你自己的域名>`，能正常显示`Hello World!`，即基础链路完全打通

### 阶段4：SSL证书异常问题解决（踩坑记录）
#### 问题现象：浏览器访问域名报错`ERR_SSL_VERSION_OR_CIPHER_MISMATCH`
#### 根因：新绑定的自定义域名，Cloudflare免费通用SSL证书尚未完成签发
#### 解决方案：

1.  临时调整：Cloudflare域名控制台→「SSL/TLS→概述」，将加密模式从「完全Full」改为**「灵活Flexible」**，等待2-3分钟生效
2.  证书验证：进入「SSL/TLS→边缘证书」，确认`*.<你自己的域名>`证书状态为「已颁发」
3.  安全回切：证书生效后，将加密模式切回「完全Full」，保障端到端通信安全

### 阶段5：Docker加速脚本部署

1.  进入Worker编辑页，删除默认的Hello World代码，粘贴开箱即用的Docker代理脚本
2.  **唯一必须修改项**：将脚本中的`workers_url`替换为自己的加速域名
    ```javascript
    // 【必须修改】替换为自己的加速域名，不要加末尾的/
    const workers_url = 'https://<docker.你自己的域名>'
    // 以下固定配置无需修改
    const hub_host = 'registry-1.docker.io'
    const auth_url = 'https://auth.docker.io'
    ```
3.  点击「保存并部署」，等待10秒生效
4.  核心接口验证命令：
    ```bash
    curl -v https://<docker.你自己的域名>/v2/
    ```
    ✅ 成功标准：返回`200 OK`或`401 Unauthorized`（Docker正常认证提示，非错误）

### 阶段6：本地Docker客户端配置与生效

1.  编辑Docker daemon配置文件：
    ```bash
    sudo vim /etc/docker/daemon.json
    ```
2.  写入加速配置（替换为自己的域名）：
    ```json
    {
      "registry-mirrors": [
        "https://<docker.你自己的域名>"
      ]
    }
    ```
3.  重启Docker使配置生效：
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    ```
4.  配置生效验证：
    ```bash
    docker info | grep -A 2 "Registry Mirrors"
    ```
    ✅ 成功标准：输出中显示自己的加速域名
5.  最终功能验证：
    ```bash
    # 测试基础镜像拉取
    docker pull hello-world
    # 测试业务镜像拉取
    docker pull bitnami/kafka:3.7.0-debian-12-r0
    ```
    ✅ 成功标准：镜像可正常、无超时拉取，加速功能完全落地

---
2. 开启 Tiered Cache（分层缓存，提升大文件命中率）

    路径：Cloudflare 控制台 → 「缓存」→「Tiered Cache」→ 开启「启用 Tiered Cache」+「智能分层」；
    作用：Cloudflare 全球节点分层缓存，大文件不用每次回源，尤其适合跨区域访问。
