package main

import (
	"encoding/json"
	"io"
	"net/http"
	"net/url"
)

// 你的AI客服接口地址
const yourAIService = "http://127.0.0.1:8080"

func main() {
	// 注册适配接口，供OpenClaw调用
	http.HandleFunc("/v1/chat/completions", adaptHandler)
	// 启动服务
	println("Go适配层运行中：http://127.0.0.1:8000")
	_ = http.ListenAndServe("127.0.0.1:8000", nil)
}

// 适配处理器：OpenAI格式 → 你的GET接口
func adaptHandler(w http.ResponseWriter, r *http.Request) {
	// 1. 解析OpenClaw的请求
	var req struct {
		Messages []struct {
			Content string `json:"content"`
		} `json:"messages"`
	}
	_ = json.NewDecoder(r.Body).Decode(&req)
	userQuery := req.Messages[len(req.Messages)-1].Content

	// 2. 调用你的GET接口：?query=xxx
	resp, err := http.Get(yourAIService + "?query=" + url.QueryEscape(userQuery))
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	defer resp.Body.Close()
	answer, _ := io.ReadAll(resp.Body)

	// 3. 封装成OpenAI标准格式返回
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]any{
		"choices": []map[string]any{
			{
				"message": map[string]string{
					"content": string(answer),
				},
			},
		},
	})
}
