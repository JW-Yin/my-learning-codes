package main

import (
	"fmt"
	"github.com/go-resty/resty/v2"
	"github.com/PuerkitoBio/goquery"
	"log"
	"time"
)

func main() {
	// 1. 创建resty客户端，请求Hacker News首页
	client := resty.New()
	client.SetTimeout(10 * time.Second)
	client.SetHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

	url := "https://news.ycombinator.com/"
	resp, err := client.R().Get(url)
	if err != nil {
		log.Fatalf("❌ 请求Hacker News失败: %v", err)
	}
	if resp.StatusCode() != 200 {
		log.Fatalf("❌ 请求失败，状态码: %d", resp.StatusCode())
	}
	defer resp.Body.Close() // 关闭响应流，避免资源泄漏

	// 2. 用goquery解析HTML响应体
	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		log.Fatalf("❌ 解析HTML失败: %v", err)
	}

	// 3. 用CSS选择器提取新闻标题（Hacker News标题结构：.titleline > a）
	fmt.Println("=== 📰 Hacker News 首页新闻标题 ===")
	doc.Find(".titleline > a").Each(func(i int, s *goquery.Selection) {
		// 获取标题文本
		title := s.Text()
		// 获取新闻链接（可选）
		link, _ := s.Attr("href")
		fmt.Printf("%d. %s\n   🔗 链接: %s\n", i+1, title, link)
	})
}
