#!/usr/bin/env python3
"""
Azure TTS Server - 简单的 HTTP 服务
提供 Azure TTS 语音合成 API
"""

import requests
import os
import subprocess
import tempfile
import logging
import secrets
from flask import Flask, request, send_file, jsonify
from io import BytesIO

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = app.logger
logger.setLevel(logging.DEBUG)

# API 认证配置 - 部署时修改此值或通过环境变量设置
API_SECRET_KEY = os.environ.get("TTS_API_KEY")
if not API_SECRET_KEY:
    # 生成随机 API Key（首次运行时）
    API_SECRET_KEY = os.environ.get("TTS_API_KEY_GENERATED", "change-me-in-production")

def check_api_key():
    """验证 API Key"""
    # 支持 URL 参数和 Header 两种方式
    api_key = request.args.get('api_key') or request.args.get('key')
    if not api_key:
        # 尝试从 Header 获取
        api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization', '').replace('Bearer ', '')

    if not api_key or api_key != API_SECRET_KEY:
        return False
    return True

# Azure 配置 - 从环境变量读取
AZURE_API_KEY = os.environ.get("AZURE_API_KEY")
AZURE_REGION = os.environ.get("AZURE_REGION", "eastasia")

if not AZURE_API_KEY:
    raise ValueError("AZURE_API_KEY 环境变量未设置，请查阅 README.md 配置说明")

# 缓存 Token
_access_token = None
_token_url = f"https://{AZURE_REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"

def get_access_token():
    global _access_token
    try:
        response = requests.post(_token_url, headers={"Ocp-Apim-Subscription-Key": AZURE_API_KEY, "Content-Length": "0"})
        if response.status_code == 200:
            _access_token = response.text
            return _access_token
    except Exception as e:
        print(f"Token 获取失败：{e}")
    return _access_token

def synthesize_speech(text, voice="zh-CN-XiaoxiaoNeural", rate="1.0", pitch="0"):
    """合成语音 - 使用 requests 调用 Azure API"""
    logger.debug(f"Synthesize called with text='{text}', voice='{voice}', rate='{rate}', pitch='{pitch}'")

    token = get_access_token()
    if not token:
        logger.error("Failed to get access token")
        return None, "Token 获取失败"

    logger.debug(f"Got token: {token[:30]}...")

    url = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
        "User-Agent": "AzureTTS-Server"
    }

    # 转换 rate 和 pitch 为 Azure 接受的格式
    # rate: 1.0 -> +0%, 1.5 -> +50%, 0.5 -> -50%
    # pitch: 数字格式 Azure 不接受，使用 default 或 Hz 格式
    try:
        rate_float = float(rate)
        if rate_float == 1.0:
            rate_str = "default"
        elif rate_float > 1.0:
            rate_str = f"+{int((rate_float - 1.0) * 100)}%"
        else:
            rate_str = f"-{int((1.0 - rate_float) * 100)}%"
    except:
        rate_str = "default"

    try:
        pitch_float = float(pitch)
        if pitch_float == 0:
            pitch_str = "default"
        elif pitch_float > 0:
            pitch_str = f"+{int(pitch_float)}Hz"
        else:
            pitch_str = f"{int(pitch_float)}Hz"
    except:
        pitch_str = "default"

    # SSML - 使用 Azure 接受的格式
    ssml = f"""<speak version='1.0' xml:lang='zh-CN'>
    <voice name='{voice}'>
        <prosody rate='{rate_str}' pitch='{pitch_str}'>{text}</prosody>
    </voice>
</speak>"""

    logger.debug(f"Sending SSML with rate='{rate_str}', pitch='{pitch_str}'")

    try:
        response = requests.post(url, headers=headers, data=ssml, timeout=30)
        logger.debug(f"Azure response: {response.status_code}, content length: {len(response.content) if response.content else 0}")

        if response.status_code == 200 and len(response.content) > 0:
            return BytesIO(response.content), None
        else:
            logger.error(f"Azure API returned {response.status_code}: {response.text[:200] if response.text else 'empty'}")
            return None, f"HTTP {response.status_code}: {response.text[:200] if response.text else 'empty'}"
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        return None, f"Request failed: {str(e)}"

@app.route('/')
def index():
    return '''
    <h1>Azure TTS Server</h1>
    <p>可用接口：</p>
    <ul>
        <li><a href="/synthesize?text=你好">/synthesize?text=文本&voice=音色&rate=1.0&pitch=0</a></li>
        <li><a href="/voices">/voices - 获取音色列表</a></li>
        <li><a href="/health">/health - 健康检查</a></li>
    </ul>
    <h3>可用音色</h3>
    <ul>
        <li>zh-CN-XiaoxiaoNeural - 晓晓 (女，温暖)</li>
        <li>zh-CN-YunxiNeural - 云希 (男，叙事)</li>
        <li>zh-CN-YunyangNeural - 云扬 (男，新闻)</li>
        <li>zh-CN-XiaoyiNeural - 晓伊 (女，活泼)</li>
    </ul>
    '''

@app.route('/synthesize')
def synthesize():
    # API 认证检查
    if not check_api_key():
        logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
        return jsonify({"error": "Unauthorized - Invalid API Key"}), 401

    text = request.args.get('text', '你好')
    voice = request.args.get('voice', 'zh-CN-XiaoxiaoNeural')
    rate = request.args.get('rate', '1.0')
    pitch = request.args.get('pitch', '0')

    audio, error = synthesize_speech(text, voice, rate, pitch)
    if error:
        return jsonify({"error": error}), 500

    return send_file(audio, mimetype='audio/mpeg')

@app.route('/voices')
def voices():
    # API 认证检查
    if not check_api_key():
        return jsonify({"error": "Unauthorized - Invalid API Key"}), 401

    voice_list = [
        {"id": "zh-CN-XiaoxiaoNeural", "name": "晓晓", "gender": "女", "style": "温暖"},
        {"id": "zh-CN-YunxiNeural", "name": "云希", "gender": "男", "style": "叙事"},
        {"id": "zh-CN-YunyangNeural", "name": "云扬", "gender": "男", "style": "新闻"},
        {"id": "zh-CN-XiaoyiNeural", "name": "晓伊", "gender": "女", "style": "活泼"},
    ]
    return jsonify(voice_list)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "token": "valid" if _access_token else "refreshing"})

if __name__ == '__main__':
    print("🚀 Azure TTS Server 启动中...")
    get_access_token()
    print("✅ Token 获取成功")
    app.run(host='0.0.0.0', port=5000, debug=False)
