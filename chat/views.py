from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import requests

@login_required
def chat_view(request):
    return render(request, 'chat/chat.html')

@require_http_methods(["POST"])
def send_message(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message')
        
        # 调用 DeepSeek API
        headers = {
            'Authorization': f'Bearer {settings.DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'messages': [
                {'role': 'user', 'content': user_message}
            ],
            'model': 'deepseek-chat',
            'temperature': 0.3,  # 降低温度值，使响应更确定性
            'max_tokens': 1000,  # 减少最大token数
            'stream': False,     # 关闭流式响应
            'top_p': 0.9,       # 添加top_p参数
            'presence_penalty': 0.1,  # 添加presence_penalty参数
            'frequency_penalty': 0.1   # 添加frequency_penalty参数
        }
        
        # 增加超时时间到60秒
        response = requests.post(
            settings.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=60  # 修改超时时间
        )
        
        if response.status_code == 200:
            api_response = response.json()
            ai_message = api_response['choices'][0]['message']['content']
            return JsonResponse({'response': ai_message})
        else:
            return JsonResponse({
                'error': f'API服务暂时不可用 (状态码: {response.status_code})'
            }, status=500)
            
    except requests.exceptions.Timeout:
        return JsonResponse({
            'error': '请求超时，请稍后重试'
        }, status=504)
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'error': f'网络连接问题，请检查网络设置'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'error': f'服务器处理错误，请稍后重试'
        }, status=500)
