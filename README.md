# Azure TTS Server

Azure 语音服务本地代理，支持多设备部署。

## 部署架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Termux    │     │      PC      │     │  SSH Home   │
│   (手机)    │     │   (笔记本)    │     │  (服务器)   │
└─────────────┘     └──────────────┘     └─────────────┘
      │                    │                    │
      └────────────────────┼────────────────────┘
                           │
                    ┌──────▼──────┐
                    │ Azure API   │
                    │ (云端)      │
                    └─────────────┘
```

## 快速启动

### 1. 安装依赖

```bash
pip install flask requests
```

### 2. 配置环境变量

```bash
export TTS_API_KEY="your-secure-api-key"
export AZURE_API_KEY="your-azure-api-key"
export AZURE_REGION="eastasia"
```

### 3. 启动服务

```bash
python3 azure_tts_server.py
```

## API 使用

### 语音合成

```bash
curl "http://localhost:5000/synthesize?text=你好&api_key=your-api-key" -o output.mp3
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| text | 要合成的文本 | 你好 |
| voice | 音色 ID | zh-CN-XiaoxiaoNeural |
| rate | 语速 (0.5-2.0) | 1.0 |
| pitch | 音调 (-50~50) | 0 |
| api_key | API 密钥 | 必填 |

### 可用音色

| 音色 ID | 名称 | 性别 | 风格 |
|--------|------|------|------|
| zh-CN-XiaoxiaoNeural | 晓晓 | 女 | 温暖 |
| zh-CN-YunxiNeural | 云希 | 男 | 叙事 |
| zh-CN-YunyangNeural | 云扬 | 男 | 新闻 |
| zh-CN-XiaoyiNeural | 晓伊 | 女 | 活泼 |

## 多设备配置

### 配置文件

复制 `config.example.json` 为 `config.json`：

```json
{
  "api_key": "throokie-azure-tts-2026",
  "azure_api_key": "your-azure-api-key",
  "azure_region": "eastasia",
  "port": 5000,
  "host": "0.0.0.0"
}
```

### 设备特定配置

| 设备 | 配置文件 | 启动命令 |
|------|----------|----------|
| PC | `config.pc.json` | `./start.sh pc` |
| Home Server | `config.home.json` | `./start.sh home` |
| Termux | `config.termux.json` | `./start.sh termux` |

## 安全提示

- ⚠️ 不要将 `config.json` 提交到 Git（已添加到 `.gitignore`）
- ⚠️ 使用环境变量存储敏感信息
- ⚠️ 定期更换 API Key

## License

MIT
