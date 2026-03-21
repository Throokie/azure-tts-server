#!/bin/bash
# Azure TTS Server - Linux 启动脚本

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
pip install flask requests --break-system-packages -q 2>/dev/null

# 创建日志目录
mkdir -p logs

# 启动服务
echo "🚀 Azure TTS Server 启动中..."
python3 azure_tts_server.py > logs/tts.log 2>&1 &
PID=$!

echo "✅ 服务启动成功 (PID: $PID)"
echo "查看日志：tail -f logs/tts.log"
echo "停止服务：kill $PID"
