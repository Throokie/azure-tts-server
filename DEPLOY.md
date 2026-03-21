# Azure TTS Server 部署指南

## 部署到 GitHub Private 仓库

### 1. 创建仓库

在 GitHub 创建 Private 仓库，例如：`yourname/azure-tts-server`

### 2. 初始化并推送

```bash
cd /tmp/azure-tts-github

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Azure TTS Server multi-device deployment"

# 添加远程仓库 (替换为你的仓库地址)
git remote add origin git@github.com:yourname/azure-tts-server.git

# 推送
git branch -M main
git push -u origin main
```

### 3. 在三台设备上部署

#### PC (笔记本)
```bash
# 克隆仓库
git clone git@github.com:yourname/azure-tts-server.git
cd azure-tts-server

# 复制配置文件
cp config.pc.json config.json

# 启动
./start.sh
```

#### SSH Home
```bash
# 克隆仓库
git clone git@github.com:yourname/azure-tts-server.git ~/azure-tts-server
cd ~/azure-tts-server

# 复制配置文件
cp config.home.json config.json

# 后台启动
nohup ./start.sh > tts.log 2>&1 &
```

#### Termux (手机)
```bash
# 克隆仓库
git clone git@github.com:yourname/azure-tts-server.git ~/azure-tts-server
cd ~/azure-tts-server

# 复制配置文件
cp config.termux.json config.json

# 启动
./start.sh termux
```

## 更新配置

当主仓库更新时：

```bash
# 在所有设备上拉取更新
git pull origin main
```

## 安全建议

1. **启用 GitHub 2FA**：保护账户安全
2. **不要提交真实 API Key**：使用 `.env` 文件存储
3. **定期更换 API Key**：修改后重新推送配置
4. **使用 Private 仓库**：防止敏感信息泄露

## 环境变量（推荐）

```bash
# 在每个设备上设置
export TTS_API_KEY="your-custom-api-key"
export AZURE_API_KEY="your-azure-api-key"
```

可以添加到 `~/.bashrc` 或 `~/.profile` 永久生效。
