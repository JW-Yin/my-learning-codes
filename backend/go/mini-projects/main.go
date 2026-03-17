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

// ======================== 请先修改这里的发件人配置 ========================
// 发件人邮箱（比如QQ邮箱、163邮箱）
const senderEmail = "926115191@qq.com"
// 邮箱SMTP授权码（不是登录密码！QQ邮箱需在设置-账户中开启SMTP并生成）
const senderAuthCode = ""
// SMTP服务器（根据邮箱类型修改，下面是QQ邮箱示例）
const smtpServer = "smtp.qq.com"
// SMTP端口（SSL加密，QQ/163邮箱都是465）
const smtpPort = 465
// ========================================================================

// SendEmail 发送邮件核心函数
// to: 收件人邮箱；subject: 邮件主题；content: 邮件内容
func SendEmail(to, subject, content string) error {
	// 1. 构造邮件头部（解决中文乱码问题）
	header := make(map[string]string)
	header["From"] = fmt.Sprintf("Go邮件脚本 <%s>", senderEmail)
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
	auth := smtp.PlainAuth("", senderEmail, senderAuthCode, smtpServer)

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
	// 1. 定义命令行参数
	var (
		to      = flag.String("to", "", "必填：目标收件人邮箱（多个用逗号分隔，如a@qq.com,b@163.com）")
		subject = flag.String("subject", "", "必填：邮件主题")
		content = flag.String("content", "", "必填：邮件内容")
	)

	// 2. 解析参数
	flag.Parse()

	// 3. 校验必填参数
	if *to == "" || *subject == "" || *content == "" {
		fmt.Println("❌ 错误：缺少必填参数！")
		fmt.Println("✅ 正确用法：")
		fmt.Println("  ./send-email --to 收件人@qq.com --subject '邮件主题' --content '邮件内容'")
		fmt.Println("✅ 示例：")
		fmt.Println("  ./send-email --to 123456@qq.com --subject '测试邮件' --content '这是Go脚本发送的测试邮件'")
		os.Exit(1)
	}

	// 4. 发送邮件
	fmt.Printf("📤 正在发送邮件到：%s\n", *to)
	err := SendEmail(*to, *subject, *content)
	if err != nil {
		fmt.Printf("❌ 邮件发送失败：%v\n", err)
		os.Exit(1)
	}

	// 5. 发送成功提示
	fmt.Printf("✅ 邮件发送成功！收件人：%s，主题：%s\n", *to, *subject)
}
