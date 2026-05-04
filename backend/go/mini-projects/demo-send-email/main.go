package main

import (
	"crypto/tls"
	"encoding/base64"
	"flag"
	"fmt"
	"net/smtp"
	"os"
	"strings"
)

// SendEmail 发送邮件核心函数
// senderEmail: 发件人邮箱；authCode: SMTP 授权码
// smtpServer: SMTP 服务器；smtpPort: SMTP 端口（通常为 465）
// to: 收件人邮箱；subject: 邮件主题；content: 邮件内容
// fromName: 发件人显示名称（可自定义）
func SendEmail(senderEmail, authCode, smtpServer string, smtpPort int, to, subject, content, fromName string) error {
	// 1. 构造邮件头部（解决中文乱码问题）
	header := make(map[string]string)
	// 发件人显示名称 + 邮箱
	if fromName != "" {
		header["From"] = fmt.Sprintf("%s <%s>", fromName, senderEmail)
	} else {
		header["From"] = fmt.Sprintf("订阅通知 <%s>", senderEmail)
	}
	header["To"] = to
	// 主题使用base64编码，避免中文乱码
	header["Subject"] = fmt.Sprintf("=?UTF-8?B?%s?=", base64Encode(subject))
	header["MIME-Version"] = "1.0"
	header["Content-Type"] = "text/plain; charset=UTF-8"

	// 2. 拼接完整邮件内容
	var mailContent strings.Builder
	for k, v := range header {
		mailContent.WriteString(fmt.Sprintf("%s: %s\r\n", k, v))
	}
	mailContent.WriteString("\r\n") // 头部和正文之间必须空一行
	mailContent.WriteString(content)

	// 3. 配置SMTP认证
	auth := smtp.PlainAuth("", senderEmail, authCode, smtpServer)

	// 4. 建立TLS加密连接（主流邮箱强制要求）
	addr := fmt.Sprintf("%s:%d", smtpServer, smtpPort)
	tlsConfig := &tls.Config{
		InsecureSkipVerify: true, // 跳过证书验证（新手友好，生产环境可关闭）
		ServerName:         smtpServer,
	}
	conn, err := tls.Dial("tcp", addr, tlsConfig)
	if err != nil {
		return fmt.Errorf("连接SMTP服务器失败: %v", err)
	}
	defer conn.Close()

	// 5. 创建SMTP客户端并发送邮件
	client, err := smtp.NewClient(conn, smtpServer)
	if err != nil {
		return fmt.Errorf("创建SMTP客户端失败: %v", err)
	}
	defer client.Close()

	// 认证
	if err := client.Auth(auth); err != nil {
		return fmt.Errorf("SMTP认证失败（检查授权码是否正确）: %v", err)
	}

	// 设置发件人
	if err := client.Mail(senderEmail); err != nil {
		return fmt.Errorf("设置发件人失败: %v", err)
	}

	// 设置收件人（支持多个收件人，用逗号分隔）
	recipients := strings.Split(to, ",")
	for _, rec := range recipients {
		if err := client.Rcpt(rec); err != nil {
			return fmt.Errorf("设置收件人%s失败: %v", rec, err)
		}
	}

	// 发送邮件内容
	w, err := client.Data()
	if err != nil {
		return fmt.Errorf("准备发送邮件内容失败: %v", err)
	}
	_, err = w.Write([]byte(mailContent.String()))
	if err != nil {
		return fmt.Errorf("发送邮件内容失败: %v", err)
	}
	err = w.Close()
	if err != nil {
		return fmt.Errorf("关闭邮件流失败: %v", err)
	}

	// 退出SMTP连接
	client.Quit()
	return nil
}

// base64Encode 对字符串进行base64编码（解决邮件主题中文乱码）
func base64Encode(s string) string {
	return base64.StdEncoding.EncodeToString([]byte(s))
}

func main() {
	// 定义所有命令行参数
	var (
		senderEmail = flag.String("sender", "", "必填：发件人邮箱（如 your@qq.com）")
		authCode    = flag.String("authcode", "", "必填：SMTP 授权码（非登录密码）")
		smtpServer  = flag.String("server", "smtp.qq.com", "SMTP 服务器地址（默认 smtp.qq.com）")
		smtpPort    = flag.Int("port", 465, "SMTP 端口（默认 465）")
		to          = flag.String("to", "", "必填：收件人邮箱（多个用逗号分隔）")
		subject     = flag.String("subject", "", "必填：邮件主题")
		content     = flag.String("content", "", "必填：邮件内容")
		fromName    = flag.String("fromname", "", "可选：发件人显示名称（默认为\"Go邮件脚本\"）")
	)

	// 解析参数
	flag.Parse()

	// 校验必填参数
	if *senderEmail == "" || *authCode == "" || *to == "" || *subject == "" || *content == "" {
		fmt.Println("❌ 错误：缺少必填参数！")
		fmt.Println("✅ 正确用法：")
		fmt.Println("  ./send-email --sender 发件人@qq.com --authcode 你的授权码 --to 收件人@qq.com --subject '主题' --content '内容' [--fromname '自定义名称']")
		fmt.Println("  可选参数：--server SMTP服务器地址 --port 端口号 --fromname 发件人显示名")
		fmt.Println("✅ 示例：")
		fmt.Println("  ./send-email --sender 123456@qq.com --authcode abcdefg12345 --to 7890@qq.com --subject '测试' --content 'Hello' --fromname '系统通知'")
		os.Exit(1)
	}

	// 发送邮件
	fmt.Printf("📤 正在发送邮件到：%s\n", *to)
	err := SendEmail(*senderEmail, *authCode, *smtpServer, *smtpPort, *to, *subject, *content, *fromName)
	if err != nil {
		fmt.Printf("❌ 邮件发送失败：%v\n", err)
		os.Exit(1)
	}

	fmt.Printf("✅ 邮件发送成功！收件人：%s，主题：%s\n", *to, *subject)
}

// 使用说明：
// ./demo \
//   --sender reminder-email@qq.com \
//   --authcode "" \
//   --to 926115191@qq.com \
//   --fromname "订阅通知" \
//   --subject "测试邮件" \
//   --content "这是通过命令行传入参数的测试邮件" \
//   --server smtp.qq.com \
//   --port 465
