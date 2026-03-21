#!/data/data/com.termux/files/usr/bin/bash
# Azure TTS Server - Termux 后台启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ .env 文件不存在，请从 .env.template 复制并配置"
    echo "cp .env.template .env"
    exit 1
fi

# 加载环境变量
export $(grep -v '^#' .env | xargs)

# 检查依赖
echo "检查依赖..."
pip install flask requests -q 2>/dev/null

# 创建日志目录
mkdir -p logs

# 后台启动服务
LOG_FILE="logs/tts-server.log"
PID_FILE="logs/tts-server.pid"

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "⚠️  服务已在运行 (PID: $OLD_PID)"
        echo "停止旧服务：./stop-termux-bg.sh"
        exit 0
    fi
fi

echo "🚀 Azure TTS Server 后台启动中..."
echo "日志文件：$LOG_FILE"

# 使用 nohup 后台运行
nohup python3 azure_tts_server.py > "$LOG_FILE" 2>&1 &
NEW_PID=$!

# 保存 PID
echo "$NEW_PID" > "$PID_FILE"

# 等待启动
sleep 2

if ps -p "$NEW_PID" > /dev/null 2>&1; then
    echo "✅ 服务启动成功 (PID: $NEW_PID)"
    echo "停止服务：./stop-termux-bg.sh"
    echo "查看日志：tail -f $LOG_FILE"
else
    echo "❌ 服务启动失败，查看日志：cat $LOG_FILE"
    exit 1
fi
