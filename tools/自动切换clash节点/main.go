package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// ===================== 核心配置 =====================
const (
	ClashController = "http://127.0.0.1:9090"
	TestTimeout     = 5 * time.Second
)

// 节点结构体
type ProxyNode struct {
	GetPath string
	PutPath string
	Name    string
}

// 你的节点列表
var nodes = []ProxyNode{
	{
		GetPath: "/proxies/%F0%9F%87%AF%F0%9F%87%B5%20%E5%85%8D%E8%B4%B9-%E6%97%A5%E6%9C%AC2-Ver.8/delay?timeout=5000&url=http:%2F%2Fwww.gstatic.com%2Fgenerate_204",
		PutPath: "/proxies/%F0%9F%94%B0%20%E9%80%89%E6%8B%A9%E8%8A%82%E7%82%B9",
		Name:    "🇯🇵 免费-日本2-Ver.8",
	},
	{
		GetPath: "/proxies/%F0%9F%87%AF%F0%9F%87%B5%20%E5%85%8D%E8%B4%B9-%E6%97%A5%E6%9C%AC5-Ver.9/delay?timeout=5000&url=http:%2F%2Fwww.gstatic.com%2Fgenerate_204",
		PutPath: "/proxies/%F0%9F%94%B0%20%E9%80%89%E6%8B%A9%E8%8A%82%E7%82%B9",
		Name:    "🇯🇵 免费-日本5-Ver.9",
	},
	{
		GetPath: "/proxies/%F0%9F%87%AF%F0%9F%87%B5%20%E5%85%8D%E8%B4%B9-%E6%97%A5%E6%9C%AC6-Ver.8/delay?timeout=5000&url=http:%2F%2Fwww.gstatic.com%2Fgenerate_204",
		PutPath: "/proxies/%F0%9F%94%B0%20%E9%80%89%E6%8B%A9%E8%8A%82%E7%82%B9",
		Name:    "🇯🇵 免费-日本6-Ver.8",
	},
	{
		GetPath: "/proxies/%F0%9F%87%AF%F0%9F%87%B5%20%E5%85%8D%E8%B4%B9-%E6%97%A5%E6%9C%AC7-Ver.2/delay?timeout=5000&url=http:%2F%2Fwww.gstatic.com%2Fgenerate_204",
		PutPath: "/proxies/%F0%9F%94%B0%20%E9%80%89%E6%8B%A9%E8%8A%82%E7%82%B9",
		Name:    "🇯🇵 免费-日本7-Ver.2",
	},
	{
		GetPath: "/proxies/%F0%9F%87%AF%F0%9F%87%B5%20%E5%85%8D%E8%B4%B9-%E6%97%A5%E6%9C%AC4-Ver.8/delay?timeout=5000&url=http:%2F%2Fwww.gstatic.com%2Fgenerate_204",
		PutPath: "/proxies/%F0%9F%94%B0%20%E9%80%89%E6%8B%A9%E8%8A%82%E7%82%B9",
		Name:    "🇯🇵 免费-日本4-Ver.8",
	},
	{
		GetPath: "/proxies/%F0%9F%87%AF%F0%9F%87%B5%20%E5%85%8D%E8%B4%B9-%E6%97%A5%E6%9C%AC3-Ver.7/delay?timeout=5000&url=http:%2F%2Fwww.gstatic.com%2Fgenerate_204",
		PutPath: "/proxies/%F0%9F%94%B0%20%E9%80%89%E6%8B%A9%E8%8A%82%E7%82%B9",
		Name:    "🇯🇵 免费-日本3-Ver.7",
	},
	{
		GetPath: "/proxies/%F0%9F%87%AF%F0%9F%87%B5%20%E5%85%8D%E8%B4%B9-%E6%97%A5%E6%9C%AC1-Ver.7/delay?timeout=5000&url=http:%2F%2Fwww.gstatic.com%2Fgenerate_204",
		PutPath: "/proxies/%F0%9F%94%B0%20%E9%80%89%E6%8B%A9%E8%8A%82%E7%82%B9",
		Name:    "🇯🇵 免费-日本1-Ver.7",
	},
}

// 公共请求头
func setCommonHeaders(req *http.Request) {
	req.Header.Set("sec-ch-ua-platform", `"Linux"`)
	req.Header.Set("Accept-Language", "zh-CN,zh;q=0.9")
	req.Header.Set("Accept", "application/json, text/plain, */*")
	req.Header.Set("sec-ch-ua", `"Not-A.Brand";v="24", "Chromium";v="146"`)
	req.Header.Set("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36")
	req.Header.Set("sec-ch-ua-mobile", "?0")
	req.Header.Set("Origin", "https://clash.razord.top")
	req.Header.Set("Sec-Fetch-Site", "cross-site")
	req.Header.Set("Sec-Fetch-Mode", "cors")
	req.Header.Set("Sec-Fetch-Dest", "empty")
	req.Header.Set("Accept-Encoding", "gzip, deflate, br")
	req.Header.Set("Connection", "keep-alive")
}

// 切换节点（不变）
func switchToNode(node ProxyNode) {
	url := ClashController + node.PutPath
	body, _ := json.Marshal(map[string]string{"name": node.Name})
	req, _ := http.NewRequest("PUT", url, bytes.NewBuffer(body))

	setCommonHeaders(req)
	req.Header.Set("Content-Type", "application/json")

	client := http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Printf("❌ 切换节点失败：%v\n", err)
		return
	}
	defer resp.Body.Close()
	io.Copy(io.Discard, resp.Body)

	fmt.Printf("\n🎉 切换成功！节点：%s\n", node.Name)
}

// 测速协程：第一个完成就发送结果，其他协程直接取消
func testNode(ctx context.Context, node ProxyNode, result chan<- ProxyNode) {
	// 创建带上下文的请求（支持取消）
	url := ClashController + node.GetPath
	req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
	setCommonHeaders(req)

	client := http.Client{Timeout: TestTimeout}
	resp, err := client.Do(req)
	if err != nil {
		return // 请求失败/被取消，直接退出
	}
	defer resp.Body.Close()

	// 解析成功，发送结果到通道（第一个到达的会被立即处理）
	var res struct{ Delay int }
	_ = json.NewDecoder(resp.Body).Decode(&res)
	if res.Delay > 0 {
		select {
		case result <- node: // 发送成功：说明是第一个完成的
		default: // 通道已关闭：说明已经有节点完成了，直接退出
		}
	}
}

func main() {
	fmt.Println("===== 第一个节点响应立即切换 =====")

	// 1. 创建可取消的上下文（用于终止所有协程）
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// 2. 创建通道：只接收第一个完成的节点
	result := make(chan ProxyNode, 1)

	// 3. 启动所有协程（并发测速）
	for _, node := range nodes {
		go testNode(ctx, node, result)
	}

	// 4. 🔥 只等待第一个结果！拿到后立刻取消所有其他请求
	bestNode := <-result
	cancel() // 秒杀所有未完成的测速协程

	// 5. 直接切换，无任何计算！
	switchToNode(bestNode)
}
