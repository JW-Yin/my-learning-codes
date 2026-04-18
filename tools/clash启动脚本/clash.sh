#!/bin/bash
# Clash 一键启动 + 等待就绪 + 自动定时优选节点 - Fedora KDE 专用
# ===================== 配置区域 =====================
CLASH_PATH="$HOME/clash"
SWITCH_BIN="$CLASH_PATH/clash-switch"
CHECK_INTERVAL=30                 # 正式5分钟，测试改5
CLASH_API="127.0.0.1:9090"
PROXY_HTTP="127.0.0.1:7890"
PROXY_SOCKS="127.0.0.1:7891"
# ====================================================

LOOP_PID=""
CLASH_PID=""
# 清理锁：保证只执行一次退出清理
CLEANUP_DONE="0"

# 关闭系统代理
unset_proxy() {
    echo -e "\n===== 正在关闭系统代理 ====="
    kwriteconfig5 --file kioslaverc --group "Proxy Settings" --key "ProxyType" 0
    kquitapp5 kio_http >/dev/null 2>&1 && kstart5 kio_http >/dev/null 2>&1
    echo "✅ 系统代理已关闭"
}

# 退出清理（加锁，只执行1次）
exit_clean() {
    if [ "$CLEANUP_DONE" = "1" ]; then
        return
    fi
    CLEANUP_DONE="1"

    unset_proxy
    # 停止定时测速
    if [ -n "$LOOP_PID" ]; then
        kill "$LOOP_PID" >/dev/null 2>&1
        echo "✅ 已停止自动测速任务"
    fi
    # 停止Clash
    if [ -n "$CLASH_PID" ]; then
        kill "$CLASH_PID" >/dev/null 2>&1
        echo "✅ 已停止Clash"
    fi
    echo "👋 程序已完全退出"
    exit 0
}

# 设置系统代理
set_proxy() {
    echo "===== 正在设置系统代理 ====="
    kwriteconfig5 --file kioslaverc --group "Proxy Settings" --key "ProxyType" 1
    kwriteconfig5 --file kioslaverc --group "Proxy Settings" --key "httpProxy" "http://$PROXY_HTTP"
    kwriteconfig5 --file kioslaverc --group "Proxy Settings" --key "socksProxy" "socks://$PROXY_SOCKS"
    kquitapp5 kio_http >/dev/null 2>&1 && kstart5 kio_http >/dev/null 2>&1
    echo "✅ 代理设置完成"
}

# 等待Clash完全启动
wait_clash_ready() {
    echo -n "===== 等待 Clash 启动就绪中"
    while ! curl -s "$CLASH_API" >/dev/null; do
        echo -n "."
        sleep 1
    done
    echo -e "\n✅ Clash 已完全启动，API 端口就绪！"
}

# 自动定时测速循环
auto_switch_loop() {
    echo "===== 启动自动测速（每 $((CHECK_INTERVAL)) 秒一次）====="
    while true; do
        echo "------------------------"
        echo -n "⏱  执行节点优选"
        "$SWITCH_BIN"
        sleep "$CHECK_INTERVAL"
    done
}

# ===================== 前置检查 =====================
if [ ! -d "$CLASH_PATH" ]; then echo "❌ Clash目录不存在"; exit 1; fi
if [ ! -f "$CLASH_PATH/clash" ]; then echo "❌ Clash程序不存在"; exit 1; fi
if [ ! -f "$SWITCH_BIN" ]; then echo "❌ 测速工具不存在"; exit 1; fi

# 捕获Ctrl+C信号（只监听一个，避免重复）
trap exit_clean INT

# ===================== 核心启动流程 =====================
set_proxy

# 后台启动Clash
echo "===== 后台启动 Clash ====="
cd "$CLASH_PATH" && ./clash -d . &
CLASH_PID=$!

# 等待Clash就绪
wait_clash_ready

# 启动后台测速任务
auto_switch_loop >> /dev/stdout 2>&1 &
LOOP_PID=$!

# 前台等待
echo "===== 所有服务启动完成，运行中 ====="
wait "$CLASH_PID"

