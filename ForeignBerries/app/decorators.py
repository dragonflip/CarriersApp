from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwards):
        if request.user.is_authenticated:
            return redirect('main')
        else:
            return view_func(request, *args, **kwards)

    return wrapper_func

def allowed_roles(allowed_roles=[]): # can pass roles which have access into param
    def decorator(view_func):
        def wrapper_func(request, *args, **kwards):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwards)

            else:
                return HttpResponse('незя')

        return wrapper_func
    return decorator

def admin_group(view_func): # only for admins
    def wrapper_function(request, *args, **kwards):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'admin':
           return view_func(request, *args, **kwards)

        else:
           return redirect('main')

    return wrapper_function

