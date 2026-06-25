# AI Chat - 智能对话助手

🚀 一个对标 ChatGPT 的全栈 AI 聊天系统，支持流式对话、Markdown 渲染、代码高亮。

## 特性

- **流式输出** — SSE 实时逐 token 推送，首字延迟 < 200ms
- **Markdown 渲染** — 代码块、表格、引用、列表全支持
- **代码高亮** — highlight.js 覆盖 12+ 编程语言
- **暗色主题** — ChatGPT 风格界面
- **免费 AI** — 接入 DeepSeek API，注册送 500 万 tokens
- **国内直连** — 无需梯子

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | HTML · CSS · JavaScript（原生，无框架） |
| 后端 | Flask（Python） · requests |
| AI | DeepSeek API / OpenAI API |
| 渲染 | marked.js · highlight.js |

## 快速开始

### 1. 获取 API Key

注册 DeepSeek（免费，送 500 万 tokens）：

https://platform.deepseek.com/

登录后进入 API Keys 页面创建一个 Key。

### 2. 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env，填入你的 Key
```

`.env` 文件内容：

```ini
DEEPSEEK_API_KEY=sk-你的密钥
```

### 3. 安装依赖

```bash
pip install flask python-dotenv requests
# 或
pip install -r requirements.txt
```

### 4. 启动

```bash
python app.py
```

打开浏览器访问 **http://localhost:5003** 🎉

## 部署到云端

### Railway（免费，推荐）

1. 把代码推送到 GitHub
2. 注册 https://railway.com ，用 GitHub 登录
3. 点 "New Project" → "Deploy from GitHub repo"
4. 选择本仓库
5. 在 Dashboard 设置环境变量：`DEEPSEEK_API_KEY=你的Key`
6. 在 Settings → Deploy 中设置启动命令：`gunicorn app:app`
7. 部署完成，自动生成 `*.railway.app` 域名

### Vercel

适合 Next.js 版本，直接连接 GitHub 仓库自动部署。

## 项目结构

```
ai-chat/
├── app.py               # Flask 后端（~90 行）
├── .env                 # API Key 配置（不要提交！）
├── .env.example         # 配置模板
├── .gitignore           # Git 忽略规则
├── requirements.txt     # Python 依赖
├── README.md            # 本文件
└── templates/
    └── index.html       # 前端页面（单文件）
```

## API 接口

```http
POST /api/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "你好"}
  ]
}
```

返回 SSE 流式响应。

## 关于简历

这个项目适合写在简历上，突出以下亮点：

- SSE 流式架构设计与实现
- 多 AI 模型兼容（DeepSeek / OpenAI 一键切换）
- 前端实时渲染（Markdown + 代码高亮）
- 双技术栈实现（Python Flask + Next.js）
- 完整的错误处理与用户体验优化
