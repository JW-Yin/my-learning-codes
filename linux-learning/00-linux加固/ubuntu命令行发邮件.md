

# Ubuntu命令行发送邮件标准化流程（基于 ssmtp + QQ邮箱）

## 一、准备工作（在邮箱网页端操作，只需做一次）
以QQ邮箱为例，其他邮箱（163、Gmail等）逻辑完全一致。

1.  登录网页版QQ邮箱 -> **设置** -> **账户**。
2.  开启 **POP3/SMTP服务** 和 **IMAP/SMTP服务**（按提示发短信验证）。
3.  点击 **生成授权码**，复制生成的**英文授权码**（不是QQ密码！），保存好。

---

## 二、在Ubuntu服务器上配置（全程复制粘贴即可）

### 1. 安装 ssmtp
```bash
# 更新软件源
sudo apt update
# 安装 ssmtp（轻量邮件发送工具）
sudo apt install ssmtp -y
```

### 2. 编辑配置文件（唯一需要修改的地方）
打开系统配置文件：
```bash
sudo vim /etc/ssmtp/ssmtp.conf
```

**操作：** 按 `ggdG` 清空文件所有内容，然后复制下面的内容进去，**注意替换成你自己的信息**：
```ssmtp
# 你的邮箱地址（用于接收系统退信等，填自己的邮箱即可）
root=你的QQ邮箱@qq.com
# SMTP服务器地址和端口（QQ邮箱固定为 smtp.qq.com:465）
mailhub=smtp.qq.com:465
# 允许在邮件内容里自定义发件人
FromLineOverride=YES
# 你的邮箱账号
AuthUser=你的QQ邮箱@qq.com
# 刚才获取的SMTP授权码（不是邮箱密码！）
AuthPass=你的SMTP授权码
# 启用SSL加密（必须）
UseTLS=YES
```

保存并退出：按 `Esc`，输入 `:wq`，回车。

---

## 三、测试发送邮件（验证配置是否成功）

### 1. 创建一封规范的测试邮件
```bash
cat > test_email.txt << EOF
From: 你的QQ邮箱@qq.com
To: 收件人邮箱@example.com
Subject: 【测试】Ubuntu邮件提醒

这是一封来自Ubuntu服务器的测试邮件，如果你收到了，说明配置成功！
EOF
```

### 2. 发送邮件
```bash
ssmtp 收件人邮箱@example.com < test_email.txt
```

**判断成功标准：** 终端没有任何输出（静默成功），且收件箱在10秒内收到邮件。

---

## 四、在Shell脚本中集成发邮件功能（通用模板）

这是一个**最小化、可直接复用**的Shell脚本发邮件示例，你可以直接复制到你的任何脚本里：

```bash
#!/bin/bash

# ================= 发邮件配置 =================
FROM_EMAIL="你的QQ邮箱@qq.com"
TO_EMAIL="收件人邮箱@example.com"
# ===========================================

# 构造邮件内容并发送
send_alert_email() {
    local email_subject="$1"
    local email_content="$2"
    
    cat > /tmp/alert_email.tmp << EOF
From: $FROM_EMAIL
To: $TO_EMAIL
Subject: $email_subject

$email_content
EOF
    
    # 发送邮件
    ssmtp "$TO_EMAIL" < /tmp/alert_email.tmp
    
    # 清理临时文件
    rm -f /tmp/alert_email.tmp
}

# ================= 调用示例 =================
# 使用方法：send_alert_email "邮件标题" "邮件内容"

# 示例1：发送简单提醒
send_alert_email "【提醒】任务执行完成" "你的脚本已经在 $(date) 执行完成了。"

# 示例2：发送带详细日志的报错提醒
ERROR_LOG="这里是详细的报错日志内容..."
send_alert_email "⚠️ 【报错】任务执行失败" "任务执行失败，详细信息如下：\n\n$ERROR_LOG"
```

---

## 五、关键注意事项（避坑指南）
1.  **授权码 vs 密码**：`AuthPass=` 必须填SMTP授权码，绝对不能填邮箱密码！
2.  **发件人必须一致**：邮件内容里的 `From:` 必须和 `AuthUser=` 的邮箱地址完全一致，否则会被SMTP服务器拒绝。
3.  **邮件头三要素**：规范的邮件必须包含 `From:`、`To:`、`Subject:` 三行，且顺序不能乱，都在邮件内容的最前面。
4.  **其他邮箱适配**：
    - 163邮箱：`mailhub=smtp.163.com:465`
    - Gmail（需科学上网）：`mailhub=smtp.gmail.com:587`，且需开启“不太安全的应用访问”
    - 企业微信邮箱：`mailhub=smtp.exmail.qq.com:465`

---

## 六、清理测试文件（可选）
配置完成后，清理测试文件：
```bash
rm -f test_email.txt
```

---
