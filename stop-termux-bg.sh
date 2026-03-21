#!/data/data/com.termux/files/usr/bin/bash
# Azure TTS Server - Termux 后台停止脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PID_FILE="logs/tts-server.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "⚠️  服务未运行 (无 PID 文件)"
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p "$PID" > /dev/null 2>&1; then
    echo "🛑 停止服务 (PID: $PID)..."
    kill "$PID"
    rm -f "$PID_FILE"
    echo "✅ 服务已停止"
else
    echo "⚠️  服务未运行 (PID: $PID 不存在)"
    rm -f "$PID_FILE"
fi
