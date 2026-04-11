package main

import (
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"github.com/go-resty/resty/v2"
	"log"
	"strings" // 新增：修复需要的包
	"time"
)

func main() {
	// 1. 创建全局HTTP客户端
	client := resty.New()
	client.SetTimeout(10 * time.Second)
	client.SetHeader("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")

	// ======================
	// 步骤1：访问登录页面
	// ======================
	loginPageURL := "http://127.0.0.1:8080/login"
	log.Println("📥 正在访问登录页面：", loginPageURL)
	resp, err := client.R().Get(loginPageURL)
	if err != nil {
		log.Fatalf("访问登录页面失败：%v", err)
	}

	// ======================
	// 步骤2：解析表单（✅ 修复点1）
	// ======================
	log.Println("\n🔍 开始提取登录表单信息...")
	// 修复：resp.Body() → 转字符串 → 转Reader
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(string(resp.Body())))
	if err != nil {
		log.Fatalf("解析HTML失败：%v", err)
	}

	// 查找登录表单
	doc.Find("form").Each(func(i int, s *goquery.Selection) {
		formAction, _ := s.Attr("action")
		formMethod, _ := s.Attr("method")
		fmt.Printf("✅ 找到登录表单：\n  提交地址：%s\n  请求方式：%s\n", formAction, formMethod)
	})

	// ======================
	// 步骤3：自动登录
	// ======================
	log.Println("\n🔐 开始自动登录...")
	loginAPI := "http://127.0.0.1:8080/api/login"
	loginData := map[string]string{
		"username":  "admin",
		"password":  "Yy1306332003",
		"recaptcha": "",
	}

	loginResp, err := client.R().
		SetHeader("Content-Type", "application/json").
		SetBody(loginData).
		Post(loginAPI)

	if err != nil || loginResp.StatusCode() != 200 {
		log.Fatalf("登录失败：%v，状态码：%d", err, loginResp.StatusCode())
	}

	// 携带Token
	token := loginResp.String()
	client.SetHeader("Authorization", "Bearer "+token)
	log.Println("✅ 登录成功！已获取Token")

	// ======================
	// 步骤4：访问首页并提取body（✅ 修复点2）
	// ======================
	log.Println("\n📄 访问登录后的首页...")
	homeResp, err := client.R().Get("http://127.0.0.1:8080/")
	if err != nil {
		log.Fatalf("访问首页失败：%v", err)
	}

	// 修复：和上面一样的写法
	homeDoc, _ := goquery.NewDocumentFromReader(strings.NewReader(string(homeResp.Body())))
	bodyContent, _ := homeDoc.Find("body").Html()

	// ======================
	// 最终输出
	// ======================
	log.Println("\n=====================================")
	log.Println("📌 登录后页面 <body> 标签内容：")
	log.Println("=====================================")
	fmt.Println(bodyContent)
}
