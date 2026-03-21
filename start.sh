#!/bin/bash
# Azure TTS Server 启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 设备配置
DEVICE="${1:-default}"

case "$DEVICE" in
    pc)
        CONFIG_FILE="config.pc.json"
        ;;
    home)
        CONFIG_FILE="config.home.json"
        ;;
    termux)
        CONFIG_FILE="config.termux.json"
        ;;
    *)
        CONFIG_FILE="config.json"
        ;;
esac

# 检查配置文件
if [ -f "$CONFIG_FILE" ]; then
    echo "使用配置文件：$CONFIG_FILE"
    export CONFIG_FROM_FILE="$CONFIG_FILE"
fi

# 安装依赖
echo "检查依赖..."
pip install flask requests -q 2>/dev/null

# 启动服务
echo "🚀 Azure TTS Server 启动中..."
echo "设备配置：$DEVICE"
python3 azure_tts_server.py
