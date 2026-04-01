# SSH免密方式配置VSCode与Gitee的联动（Ubuntu 22.04版）


## 一、基础前置配置
1. 安装必备工具：VSCode（官网下载安装）+ Git（Ubuntu终端执行）
   ```bash
   sudo apt update && sudo apt install git -y
   ```
2. 配置Git全局用户名/邮箱（记录提交身份，与Gitee绑定信息一致最佳）
   ```bash
   git config --global user.name "你的Gitee用户名/自定义名称"
   git config --global user.email "你的Gitee绑定邮箱"
   ```
3. 验证Git安装与配置：执行后能输出版本+配置信息即完成
   ```bash
   git --version && git config --list
   ```

## 二、SSH密钥免密配置
**核心**：本地生成密钥对，公钥上传Gitee，实现Git/VSCode与Gitee免密通信，避免反复输账号密码

1. 本地生成ED25519密钥对（终端执行，提示输入密码时直接回车，无需设置）
   ```bash
   ssh-keygen -t ed25519 -C "你的Gitee绑定邮箱"
   ```
2. 设置密钥严格权限（Git/SSH强制要求，否则连接失败，必做）
   ```bash
   chmod 600 ~/.ssh/id_ed25519  # 私钥仅当前用户读写
   chmod 644 ~/.ssh/id_ed25519.pub  # 公钥允许其他用户读
   ```
3. 复制本地公钥内容（直接复制终端输出的完整内容，无删减）
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
4. 公钥上传Gitee：Gitee官网→登录→右上角头像「设置」→「SSH公钥」→粘贴公钥内容→自定义标题（如Ubuntu）→「添加公钥」（验证Gitee密码即可）

5. 验证SSH连接（核心步骤，确认密钥生效）：终端执行，出现指定提示即成功
   ```bash
   ssh -T git@gitee.com
   ```
   成功则提示：`Hi 你的Gitee用户名! You've successfully authenticated, but Gitee.com does not provide shell access.`

## 三、项目联动（Gitee已有远程仓库，本地拉取并与VSCode绑定）
**核心**：`git clone` 一键完成「本地仓库初始化+绑定远程仓库+同步远程文件」，**无需额外执行git init**

1. 复制Gitee远程仓库SSH地址：Gitee仓库页面→「克隆/下载」→选择「SSH」→复制地址（格式：`git@gitee.com:用户名/仓库名.git`）

2. 终端执行SSH克隆，拉取远程仓库到本地指定文件夹（如桌面my-learning-codes）
   ```bash
   git clone 你复制的Gitee SSH地址 ~/桌面/my-learning-codes
   ```

   克隆成功：终端显示「Receiving objects: 100%」，本地文件夹生成隐藏的`.git`文件夹（Ubuntu按Ctrl+H可查看）

3. VSCode绑定本地仓库：打开VSCode→「文件」→「打开文件夹」→选择克隆后的本地文件夹（如my-learning-codes）→「打开」
   联动完成：VSCode左侧自动出现「源代码管理」面板，识别Git仓库及已绑定的远程仓库（origin）
