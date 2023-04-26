from datetime import datetime
from django.http import JsonResponse


def server_check(request):
    return JsonResponse({
        'now': datetime.now()
    })
