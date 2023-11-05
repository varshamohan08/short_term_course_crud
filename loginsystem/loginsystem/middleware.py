from django.shortcuts import redirect
from django.contrib.auth import logout

class userLogMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 'Email': 'b@g.com', 'Password': 'test@123456'
        path = request.path_info.lstrip('/')
        if path in ['login']:
            return self.get_response(request)
        else:
            if request.user and request.user.id:
                return self.get_response(request)
            else:
                return redirect('http://127.0.0.1:8000/login')
