# 👋 你好，我是殷佳伟  
> 计算机科学与技术专业 | 算法竞赛国奖 | Java Web全栈开发 | Linux运维 | 云原生安全/DevSecOps深耕者  
> 
> 核心目标：深耕 Java后端 / Go / Linux / Docker / K8s / 容器运行时安全 / Operator / 准入控制器 / Trivy/Falco 二次开发，立志成为「懂开发的云原生安全专家」
> 
> 邮箱：JW-Yin@foxmail.com | 电话：198-3328-8907（微信同号）
---

## 🏆 核心成果与荣誉
### 竞赛获奖（国家级/省级）
- 2024 蓝桥杯全国软件和信息技术专业人才大赛 C/C++ 组 **全国二等奖**
- 2024 河北省大学生程序设计竞赛（HBCPC，ACM赛制）**二等奖**
- 2024 全国大学生数学竞赛（CMC）**省级二等奖**
- 2023 全国大学生数字技能应用大赛 Java 组 **全国二等奖**
- 2024 全国大学生数字技能应用大赛 C 语言组 **全国三等奖**
- 2023 CSDN杯Web前端设计大赛 **二等奖**
- 2023 河北省“先控杯”节能减排大赛 **三等奖**
- 连续三年获专业二、三等奖学金，GPA 3.60，专业前20%

### 实习与工程实践
- 北京直真科技股份有限公司 | Linux运维实习生
  - 负责Linux服务器日常运维与监控，协助部署MySQL主从集群、Kafka/Zookeeper等高可用中间件（云原生基础组件实践）
  - 完成TiDB集群Docker环境部署与基础验证，支撑国产化迁移技术预研（容器化部署实战）
  - 协助搭建基于Ollama+AnythingLLM的私有化文档检索系统，实现本地知识库智能问答

### 基础能力沉淀
- CET-4、工业互联网平台开发工程师（初级）、全国计算机等级考试二级、普通话二甲
- 算法能力：Codeforces 1700分水平，熟练使用C/C++实现算法设计与程序优化
- 安全基础：掌握Web安全核心漏洞原理（SQL注入/XSS/文件上传），搭建本地靶场完成复现，为云原生安全漏洞分析提供基础支撑

---

## 🚀 核心项目作品
### 1. 乡村振兴助农电商系统（毕业设计）
**技术栈**：Java、SpringBoot、MyBatis、MySQL/TiDB、Thymeleaf、FastAPI、RAG、Docker  

**核心亮点**：
- 独立开发全栈，实现商品展示、订单管理、用户权限等核心模块，后端基于SpringBoot构建RESTful API，前端通过Thymeleaf+AJAX实现动态渲染
- 完成MySQL到TiDB分布式集群的迁移优化，经JMeter压测验证，系统TPS提升30%，产出完整的性能对比测试报告
- 基于RAG架构封装AI智能客服，通过FastAPI搭建独立服务，与SpringBoot后端打通，实现商品咨询、助农政策智能问答
- 基于Docker Compose实现多服务一键容器化部署与环境隔离，掌握容器化应用交付核心能力（云原生基础实践）  

**仓库导航**：[如需查看源码，可邮件/微信联系我](./agriculture-ecommerce)

### 2. 自动化Web漏洞扫描器（基础安全能力沉淀）
**技术栈**：Python、requests、BeautifulSoup、threading、argparse、logging

**核心亮点**：
- 自主开发的自动化渗透测试工具，支持SQL注入、XSS跨站脚本、文件上传等常见漏洞的自动化检测
- 基于threading+任务队列实现多线程并发扫描，可灵活控制并发速率，兼顾扫描效率与目标服务器稳定性
- 支持自定义命令行参数配置，自动生成结构化JSON格式检测报告，完整记录漏洞触发payload、风险等级与修复建议
- 完成DVWA靶场low/medium级别全漏洞通关验证，为云原生应用层安全分析夯实基础  

**仓库导航**：[如需查看源码，可邮件/微信联系我](./web-vulnerability-scanner)

---

## 🛠️ 技术栈全景
| 技术领域 | 核心技能点 |
|----------|------------|
| **编程语言** | Go（重点学习）、C/C++（CF 1700算法水平）、Java、Python、Shell |
| **云原生核心** | Docker（容器化部署/镜像优化）、K8s（基础架构/资源配置）、Operator（入门）、准入控制器（Demo级实践） |
| **云原生安全** | 运行时安全（Falco规则编写入门）、漏洞扫描（Trivy二次开发）、容器安全加固、K8s安全配置 |
| **后端开发** | Java Web（Spring Boot、MyBatis、Thymeleaf）、Python Web（FastAPI）、RESTful API设计（为Operator开发打基础） |
| **数据库** | MySQL、TiDB、数据库主从架构搭建、SQL性能优化 |
| **系统运维** | Linux内核基础、SSH安全加固、Shell自动化脚本、中间件部署（Kafka/Zookeeper） |
| **工具与工程能力** | Git、JMeter压测、Docker Compose、日志系统设计、多线程编程 |

---

## 📚 学习轨迹与仓库导航
本仓库按**技术领域**分类管理学习内容，聚焦**云原生安全/DevSecOps**核心方向，同时覆盖算法、后端、AI等基础能力沉淀，所有内容均配套可运行代码与实战笔记：

### 核心深耕领域：devsecops/（云原生安全/DevSecOps）
这是未来三年的核心学习方向，按「底层基础→容器技术→编排调度→安全工具链」分层推进：
- **[devsecops/linux/](./devsecops/linux)**：Linux 全栈能力（由浅入深）
  - `administration/`：Linux 运维管理（基础命令、systemd、网络配置、Shell 自动化脚本）
  - `system-programming/`：Linux 系统编程（C 语言实现文件/进程/IPC，为容器底层原理打基础）
  - `kernel/`：Linux 内核基础（内核模块、eBPF 入门，为云原生运行时安全赋能）
- **[devsecops/container/](./devsecops/container)**：容器技术核心
  - `docker/`：Docker 使用与原理（镜像构建/优化/安全最佳实践、容器攻击面识别）
  - `runtime/`：容器运行时（containerd、runc 原理，为容器安全加固奠基）
- **[devsecops/kubernetes/](./devsecops/kubernetes)**：Kubernetes 核心与安全
  - `basics/`：K8s 基础概念、YAML 编写、集群搭建与故障排查
  - `operator/`：Operator 开发（Operator SDK、client-go 实战）
  - `security/`：K8s 安全（RBAC/NetworkPolicy/准入控制器、CIS 基准加固）
- **[devsecops/security-tools/](./devsecops/security-tools)**：云原生安全工具链
  - `trivy/`：镜像漏洞扫描（二次开发、企业级报告定制）
  - `falco/`：运行时安全（自定义告警规则、容器入侵检测）
  - `kube-bench/`：K8s 配置安全检查
  - `custom/`：自研云原生安全小工具（准入控制器、扫描脚本等）

### 基础能力支撑领域
- **[algorithms/](./algorithms)**：算法与数据结构（通用基础，为 Go/Java 开发、安全工具逻辑设计赋能）
  - `c-cpp/`：C/C++ 实现（排序、链表、树、LeetCode/Codeforces 刷题）
  - `python/`、`java/`：其他语言实现（可选）
- **[backend/](./backend)**：后端开发能力沉淀（为 Operator 开发、安全工具后端奠基）
  - `java/`：Java 后端（Spring Boot、MyBatis 实战，业务开发能力复用）
  - `go/`：Go 后端（Gin、标准库，云原生开发首选语言）
  - `python/`：Python 后端（FastAPI，AI 服务对接能力）
  - `message-queue/`：消息队列（Kafka 等，云原生中间件基础）
- **[ai/](./ai)**：人工智能拓展（RAG 等技术为安全知识库赋能，可选）
  - `libs/`：AI 库学习（transformers、langchain、torch）
  - `mini-projects/`：小型 AI 项目（图像分类、文本生成 Demo）
  - `projects/`：完整 AI 项目（RAG、Agent 等）
- **[tools/](./tools)**：通用工具配置（跨领域效率提升）
  - `git/`：Git 钩子、配置
  - `vim/`：Vim 配置
  - `shell/`：通用 Shell 脚本（非运维专用）

> 🚧 本仓库以 **devsecops/** 为核心持续更新，其他领域为基础能力支撑。后续将重点补充 K8s Operator 开发、Falco 规则定制、Trivy 二次开发等实战内容，如需深入交流可通过邮件/微信联系～

---

🎯 分阶段成长规划（研0-研3）

核心理念：**先云原生基础，再安全专项；先实操落地，再理论深化**，拒绝空泛，所有阶段均有可验收标准。

### 1. 筑基期（研0，当前阶段）

- **核心目标**：打牢Go、Linux容器、Docker、K8s基础，建立云原生安全意识
- **落地任务**：
  - 系统学习Go语言（语法→并发→client-go），完成3个以上小工具开发（如K8s Pod信息查询）
  - 深入理解Linux Namespace/Cgroup，实操nsenter/strace调试容器
  - 熟练Docker安全最佳实践，完成Java Web项目容器化安全改造
  - 搭建minikube/k3s集群，熟悉K8s核心资源与基础操作
- **验收标准**：完成Trivy二次开发Demo、输出10+篇技术笔记、能独立排查容器/K8s基础故障
  
  ### 2. 云原生核心期（研1上）
  
- **核心目标**：吃透K8s核心原理，入门Operator与准入控制器
- **落地任务**：
  - 深耕K8s安全组件（RBAC/NetworkPolicy/准入控制器），编写自定义准入控制器拦截高危Pod
  - 入门Operator SDK，开发1个简易Operator（如自定义资源管理容器安全策略）
  - 完成K8s CIS基准加固，用kube-bench扫描并修复配置风险
- **验收标准**：自定义准入控制器上线验证、输出K8s安全配置实战手册、完成1篇K8s源码阅读笔记
  
  ### 3. 安全融合期（研1下-研2）
  
- **核心目标**：融合安全能力与云原生技术，落地DevSecOps工具链
- **落地任务**：
  - 部署Falco并自定义容器异常行为告警规则，实现运行时入侵检测
  - 集成Trivy/Checkov到GitLab CI，实现漏洞扫描与流水线阻断
  - 二次开发Trivy/Falco（如扩展漏洞规则、定制告警输出）
- **验收标准**：DevSecOps流水线落地、完成企业级云原生漏洞扫描工具Demo、输出1篇云原生漏洞分析文章
  
  ### 4. 体系深化期（研2-研3）
  
- **核心目标**：全链路实战，冲刺校招
- **落地任务**：
  - 复现2-3个主流云原生安全漏洞，编写防御方案
  - 完成核心开源项目（如「基于Go+K8s+Falco的运行时安全防护平台」），落地GitHub并编写完整文档
  - 投递云原生安全/DevSecOps实习，积累企业级经验
  - 备战CKS认证，梳理面试高频考点
- **验收标准**：拿到目标方向实习/校招offer、向开源社区提交1-2个PR、获取CKS认证（可选）
---

## 📫 联系我
- 邮箱：JW-Yin@foxmail.com
- 电话：198-3328-8907（微信同号）

> 🚧 本仓库聚焦云原生安全/DevSecOps领域持续更新，所有项目均为实战驱动，如需深入交流技术方向或获取完整源码，欢迎随时联系～