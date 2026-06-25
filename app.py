import os
import json
import requests
from flask import Flask, request, Response, stream_with_context, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# DeepSeek 配置
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'
DEEPSEEK_MODEL = 'deepseek-chat'

SYSTEM_PROMPT = '你是一个智能 AI 助手，名叫 ChatAI。你用中文回答用户的问题。你的回答清晰、准确、有条理。当用户问技术问题时，你可以提供代码示例。请用 Markdown 格式组织你的回答，使内容更易读。'

# 代理配置（可选）
PROXY = os.getenv('HTTPS_PROXY') or os.getenv('HTTP_PROXY')


@app.route('/')
def index():
    return render_template('index.html', has_key=bool(DEEPSEEK_API_KEY))


@app.route('/api/chat', methods=['POST'])
def chat():
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == 'sk-你的DeepSeek密钥':
        return {'error': '请先配置 DeepSeek API Key（免费注册: https://platform.deepseek.com/）'}, 401

    data = request.get_json()
    messages = data.get('messages', [])
    if not messages:
        return {'error': '消息不能为空'}, 400

    # 构造请求
    body = {
        'model': DEEPSEEK_MODEL,
        'messages': [{'role': 'system', 'content': SYSTEM_PROMPT}] + messages,
        'stream': True,
        'max_tokens': 4096,
        'temperature': 0.7,
    }

    def generate():
        try:
            resp = requests.post(
                DEEPSEEK_API_URL,
                headers={
                    'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
                    'Content-Type': 'application/json',
                },
                json=body,
                stream=True,
                timeout=60,
                proxies={'https': PROXY, 'http': PROXY} if PROXY else None,
            )

            if resp.status_code != 200:
                err = resp.json().get('error', {})
                msg = err.get('message', f'API 返回错误 ({resp.status_code})')
                yield f'data: {json.dumps({"error": msg})}\n\n'
                yield 'data: [DONE]\n\n'
                return

            for line in resp.iter_lines():
                if not line:
                    continue
                line = line.decode('utf-8')
                if not line.startswith('data: '):
                    continue
                data = line[6:]
                if data == '[DONE]':
                    yield 'data: [DONE]\n\n'
                    return
                try:
                    chunk = json.loads(data)
                    content = chunk.get('choices', [{}])[0].get('delta', {}).get('content', '')
                    if content:
                        yield f'data: {json.dumps({"content": content})}\n\n'
                except json.JSONDecodeError:
                    continue

        except requests.exceptions.ConnectionError:
            yield f'data: {json.dumps({"error": "无法连接到 DeepSeek 服务器，请检查网络"})}\n\n'
            yield 'data: [DONE]\n\n'
        except requests.exceptions.Timeout:
            yield f'data: {json.dumps({"error": "请求超时，请稍后重试"})}\n\n'
            yield 'data: [DONE]\n\n'
        except Exception as e:
            yield f'data: {json.dumps({"error": f"服务器错误: {str(e)}"})}\n\n'
            yield 'data: [DONE]\n\n'

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        }
    )


if __name__ == '__main__':
    print(f'🤖 AI Chat 已启动: http://localhost:5003')
    print(f'📝 DeepSeek API Key: {"已配置" if DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "sk-你的DeepSeek密钥" else "未配置"}')
    app.run(host='0.0.0.0', port=5003, debug=True, threaded=True)
