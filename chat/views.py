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
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(
            settings.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            api_response = response.json()
            ai_message = api_response['choices'][0]['message']['content']
            return JsonResponse({'response': ai_message})
        else:
            return JsonResponse({
                'error': f'API错误: {response.status_code}'
            }, status=500)
            
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'error': f'网络错误: {str(e)}'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'error': f'服务器错误: {str(e)}'
        }, status=500)
