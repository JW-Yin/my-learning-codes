package main

import (
	"fmt"
	"github.com/go-co-op/gocron/v2"
	"time"
)

// 任务函数：打印格式化的当前时间
func printCurrentTime() {
	fmt.Printf("当前时间：%s\n", time.Now().Format("2006-01-02 15:04:05"))
}

func main() {
	// 1. 创建调度器（新版本支持时区、并发等更多配置）
	s, err := gocron.NewScheduler()
	if err != nil {
		panic(fmt.Sprintf("创建调度器失败: %v", err))
	}

	// 2. 定义任务：每5秒执行一次printCurrentTime
	_, err = s.NewJob(
		gocron.DurationJob(2*time.Second), // 时间间隔：5秒
		gocron.NewTask(printCurrentTime),  // 绑定任务函数
	)
	if err != nil {
		panic(fmt.Sprintf("添加任务失败: %v", err))
	}

	// 3. 原生异步启动调度器
	s.Start()
	fmt.Println("定时任务已启动，每5秒打印时间...")

	// 4. 阻塞主程序
	select {}
}
