package main

import (
	"fmt"
	"github.com/go-resty/resty/v2"
	"log"
	"time"
)

func main() {
	// 1. 创建 resty 客户端（复用，性能更好）
	client := resty.New()
	client.SetTimeout(10 * time.Second)
	// 完全照搬你浏览器的请求头（反爬/兼容必备）
	client.SetHeaders(map[string]string{
		"User-Agent":        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
		"Accept":            "*/*",
		"Accept-Language":   "zh-CN,zh;q=0.9",
		"sec-ch-ua-platform": `"Linux"`,
		"sec-ch-ua":         `"Not-A.Brand";v="24", "Chromium";v="146"`,
		"sec-ch-ua-mobile":  "?0",
		"Origin":            "http://127.0.0.1:8080",
		"Referer":           "http://127.0.0.1:8080/login?redirect=/files/ping",
		"Content-Type":      "application/json", // 关键：JSON 请求
	})

	// 2. 登录请求：发送 JSON 用户名密码
	loginURL := "http://127.0.0.1:8080/api/login"
	loginBody := map[string]string{
		"username":  "admin",
		"password":  "Yy1306332003",
		"recaptcha": "",
	}

	// 发送 POST 请求
	resp, err := client.R().
		SetBody(loginBody). // 自动序列化为 JSON
		Post(loginURL)

	if err != nil {
		log.Fatalf("登录请求失败: %v", err)
	}

	// 打印登录结果
	fmt.Printf("登录状态码: %d\n", resp.StatusCode())
	fmt.Printf("登录返回的 JWT Token:\n%s\n", resp.String())

	// 3. 核心：把 Token 存入请求头，后续所有请求自动携带
	client.SetHeader("Authorization", "Bearer "+resp.String())

	// 4. 访问需要登录的接口（测试：/files/ping）
	protectedURL := "http://127.0.0.1:8080/files/ping"
	protectedResp, err := client.R().Get(protectedURL)
	if err != nil {
		log.Fatalf("访问受保护接口失败: %v", err)
	}

	fmt.Println("\n===== 登录成功，访问受保护接口结果 =====")
	fmt.Printf("状态码: %d\n", protectedResp.StatusCode())
	fmt.Println("响应内容:", protectedResp.String())
}
