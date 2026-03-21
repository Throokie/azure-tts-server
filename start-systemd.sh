#!/bin/bash
# Azure TTS Server - Linux systemd 后台启动脚本
# 用于 PC 和 SSH Home 部署

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "❌ .env 文件不存在，请从 .env.template 复制并配置"
    echo "cp .env.template .env"
    exit 1
fi

# 检查是否 root
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  请使用 sudo 运行此脚本"
    echo "sudo $0"
    exit 1
fi

SERVICE_NAME="azure-tts-server"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

# 创建 systemd 服务文件
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Azure TTS Server
After=network.target

[Service]
Type=simple
User=$SUDO_USER
WorkingDirectory=$SCRIPT_DIR
EnvironmentFile=$SCRIPT_DIR/.env
ExecStart=/usr/bin/python3 $SCRIPT_DIR/azure_tts_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "✅ systemd 服务文件已创建：$SERVICE_FILE"

# 重载 systemd
systemctl daemon-reload

# 启用并启动服务
systemctl enable "$SERVICE_NAME"
systemctl start "$SERVICE_NAME"

echo ""
echo "✅ Azure TTS Server 已安装为系统服务"
echo ""
echo "服务管理命令："
echo "  启动服务：sudo systemctl start $SERVICE_NAME"
echo "  停止服务：sudo systemctl stop $SERVICE_NAME"
echo "  重启服务：sudo systemctl restart $SERVICE_NAME"
echo "  查看状态：systemctl status $SERVICE_NAME"
echo "  查看日志：journalctl -u $SERVICE_NAME -f"
