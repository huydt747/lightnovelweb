from django.shortcuts import render
from django.utils.translation import get_language, activate
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    user_language = get_language()
    print(f"Current language: {user_language}")
    
    context = {
        'current_language': user_language,
        'available_languages': [
            {'code': 'vi', 'name': 'Tiếng Việt'},
            {'code': 'en', 'name': 'English'},
        ]
    }
    
    return render(request, 'index.html', context)

@require_POST
@csrf_exempt
def set_language(request):
    """Custom view để thay đổi ngôn ngữ qua AJAX"""
    try:
        data = json.loads(request.body)
        language_code = data.get('language')
        
        if language_code:
            activate(language_code)
            request.session['django_language'] = language_code
            return JsonResponse({'status': 'success', 'language': language_code})
    except:
        pass
    
    return JsonResponse({'status': 'error'})