# Azure TTS Server - 快速部署指南

## 📦 已部署设备

| 设备 | 地址 | 端口 | 启动方式 |
|------|------|------|----------|
| **PC (笔记本)** | localhost | 5000 | `~/azure-tts-server/start.sh` |
| **Home Server** | 192.168.31.223 | 5000 | `~/azure-tts-server/start.sh` |
| **Termux (手机)** | 192.168.1.12:8022 | 5000 | `~/azure-tts-server/start-termux-bg.sh` |

## 🔑 API 配置

**TTS_API_KEY**: `b9a24510db9b7938093ccad6a16f799d`

**Azure API Key**: 已配置在 `.env` 文件

## 🚀 启动命令

### PC / Home Server
```bash
cd ~/azure-tts-server
./start.sh
```

### Termux (后台运行)
```bash
cd ~/azure-tts-server
./start-termux-bg.sh

# 停止服务
./stop-termux-bg.sh

# 查看日志
tail -f logs/tts-server.log
```

## 🔗 API 端点

| 端点 | 说明 | 示例 |
|------|------|------|
| `/health` | 健康检查 | `curl http://localhost:5000/health` |
| `/synthesize?text=xxx` | 语音合成 | `curl "http://localhost:5000/synthesize?text=你好"` |
| `/voices` | 音色列表 | `curl http://localhost:5000/voices` |

### 带 API 认证
```bash
# URL 参数方式
curl "http://localhost:5000/synthesize?text=你好&api_key=b9a24510db9b7938093ccad6a16f799d"

# Header 方式
curl -H "X-API-Key: b9a24510db9b7938093ccad6a16f799d" "http://localhost:5000/synthesize?text=你好"
```

## 📱 可用音色

| ID | 名称 | 性别 | 风格 |
|----|------|------|------|
| zh-CN-XiaoxiaoNeural | 晓晓 | 女 | 温暖 |
| zh-CN-YunxiNeural | 云希 | 男 | 叙事 |
| zh-CN-YunyangNeural | 云扬 | 男 | 新闻 |
| zh-CN-XiaoyiNeural | 晓伊 | 女 | 活泼 |

## 🔧 环境变量

编辑 `.env` 文件：
```bash
TTS_API_KEY="your-api-key"
AZURE_API_KEY="your-azure-api-key"
AZURE_REGION="eastasia"
```
