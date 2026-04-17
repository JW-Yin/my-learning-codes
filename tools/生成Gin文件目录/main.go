// setup.go
// 用法: go run setup.go
// 功能: 在当前目录创建符合最佳实践的三容器项目结构，并生成 README.md
package main

import (
	"fmt"
	"os"
	"path/filepath"
)

// 定义要创建的目录
var dirs = []string{
	"frontend/css",
	"frontend/js",
	"frontend/assets",
	"backend/cmd/server",
	"backend/configs",
	"backend/internal/config",
	"backend/internal/handler",
	"backend/internal/service",
	"backend/internal/repository",
	"backend/internal/model",
	"backend/internal/middleware",
	"backend/internal/router",
	"backend/internal/database",
	"backend/pkg/logger",
	"backend/pkg/response",
	"backend/migrations",
	"scripts",
}

// 定义要创建的文件及其内容（全部使用反引号原始字符串，无需转义）
var files = map[string]string{
	"frontend/Dockerfile": `# 前端 Dockerfile 占位，请根据实际构建步骤填写`,
	"frontend/nginx.conf": `# Nginx 配置占位，用于 SPA 回退和 API 代理`,
	"frontend/index.html": `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>App</title>
</head>
<body>
</body>
</html>`,
	"backend/Dockerfile":    `# 后端 Dockerfile 占位，多阶段构建 Go 服务`,
	"backend/entrypoint.sh": `#!/bin/sh\necho "Entrypoint placeholder"`,
	"backend/cmd/server/main.go": `package main

func main() {
	// 启动 Gin 服务
}`,
	"backend/configs/config.yaml": `server:
  port: 8080
database:
  host: localhost
  port: 5432
  user: postgres
  password: secret
  dbname: myapp
  sslmode: disable`,
	"backend/migrations/000001_init.up.sql":   `-- 初始表结构（基调）\nCREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT);`,
	"backend/migrations/000001_init.down.sql": `-- 回滚初始表结构\nDROP TABLE IF EXISTS users;`,
	".gitignore":         `/.idea\n/.vscode\n*.log\n.env\nfrontend/dist\nbackend/static`,
	".dockerignore":      `**/.git\n**/node_modules\n*.log\n.env`,
	"docker-compose.yml": `# 三容器编排文件占位`,
}

// README 内容模板（原始字符串，直接包含代码块）
const readmeContent = `# 项目结构说明

## 技术栈
- 前端：HTML / CSS / JavaScript + Fetch API
- 后端：Gin + GORM + PostgreSQL + Viper + slog
- 部署：Docker + Docker Compose（三容器模式）

## 目录结构

` + "```" + `
project/
├── .gitignore
├── .dockerignore
├── docker-compose.yml            # 编排 db、backend、frontend 三个容器
├── README.md
│
├── frontend/                     # 前端源码（纯静态 + Nginx）
│   ├── Dockerfile                # 前端镜像：构建产物 → Nginx 托管
│   ├── nginx.conf                # Nginx 配置（SPA 回退、API 代理）
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── backend/                      # 后端 Go 项目
│   ├── Dockerfile                # 后端镜像：编译 Go → 运行二进制
│   ├── entrypoint.sh             # 启动脚本：等数据库 → 执行迁移 → 启动服务
│   ├── go.mod
│   ├── go.sum
│   ├── cmd/
│   │   └── server/
│   │       └── main.go
│   ├── configs/
│   │   └── config.yaml
│   ├── internal/
│   │   ├── config/               # Viper 加载配置
│   │   ├── handler/              # Gin 处理器
│   │   ├── service/              # 业务逻辑
│   │   ├── repository/           # GORM 数据操作
│   │   ├── model/                # GORM 模型
│   │   ├── middleware/           # CORS、日志等
│   │   ├── router/               # 路由注册（纯 API）
│   │   └── database/             # GORM 初始化
│   ├── pkg/
│   │   ├── logger/               # slog 封装
│   │   └── response/             # 统一 JSON 响应
│   └── migrations/               # 数据库迁移文件（版本控制）
│       ├── 000001_init.up.sql    # 初始表结构（“基调”）
│       └── 000001_init.down.sql
│
└── scripts/                      # 开发辅助脚本
` + "```" + `

## 分层职责

### 前端容器 (frontend)
- 使用 Nginx 托管静态资源。
- 通过反向代理将 ` + "`/api/*`" + ` 请求转发给后端容器。
- 支持单页应用（SPA）路由回退。

### 后端容器 (backend)
- 基于 Gin 提供 RESTful API。
- 启动时通过 ` + "`entrypoint.sh`" + ` 等待 PostgreSQL 就绪，并执行 ` + "`migrations/`" + ` 中的 SQL 迁移。
- 不托管前端静态文件，职责单一。

### 数据库容器 (db)
- 使用官方 ` + "`postgres:16-alpine`" + ` 镜像。
- 数据持久化通过 Docker Volume 实现。
- 仅提供空数据库，表结构由后端迁移工具创建。

## 迁移文件管理
- ` + "`backend/migrations/`" + ` 目录存放所有数据库结构变更。
- 每个迁移包含 ` + "`.up.sql`" + ` 和 ` + "`.down.sql`" + `，支持版本升级与回滚。
- 原理类似于 Git，保证表结构变更可追溯、可复现、可回滚。

## 启动方式
` + "```bash" + `
# 在项目根目录执行
docker-compose up -d
` + "```" + `

访问 http://localhost 即可使用。

## 开发工作流建议
1. 修改后端模型后，同步编写对应的迁移 SQL 文件。
2. 前端独立开发时可使用 Live Server 或 ` + "`npm run dev`" + `，并配置代理到后端 API 地址。
3. 提交代码前确保迁移文件已纳入版本控制。
`

func main() {
	// 创建目录
	for _, d := range dirs {
		if err := os.MkdirAll(d, 0755); err != nil {
			fmt.Printf("创建目录失败 %s: %v\n", d, err)
			return
		}
		fmt.Printf("✓ 目录: %s\n", d)
	}

	// 创建文件并写入内容
	for path, content := range files {
		// 确保父目录存在
		dir := filepath.Dir(path)
		if dir != "." {
			if err := os.MkdirAll(dir, 0755); err != nil {
				fmt.Printf("创建父目录失败 %s: %v\n", dir, err)
				return
			}
		}
		if err := os.WriteFile(path, []byte(content), 0644); err != nil {
			fmt.Printf("创建文件失败 %s: %v\n", path, err)
			return
		}
		fmt.Printf("✓ 文件: %s\n", path)
	}

	// 写入 README.md
	if err := os.WriteFile("README.md", []byte(readmeContent), 0644); err != nil {
		fmt.Printf("写入 README.md 失败: %v\n", err)
		return
	}
	fmt.Println("✓ README.md 已生成")

	// 给 entrypoint.sh 添加执行权限（Unix 系统下有效）
	entrypointPath := "backend/entrypoint.sh"
	if err := os.Chmod(entrypointPath, 0755); err == nil {
		fmt.Println("✓ 已设置 entrypoint.sh 可执行权限")
	} else {
		fmt.Printf("⚠ 设置执行权限失败（Windows 下可忽略）: %v\n", err)
	}

	fmt.Println("\n✅ 项目结构初始化完成！")
	fmt.Println("提示：所有占位文件均可直接编辑，无需手动清理。")
	fmt.Println("下一步：进入 backend/ 目录执行 go mod init <模块名>")
}
