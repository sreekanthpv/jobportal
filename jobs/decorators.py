from django.shortcuts import redirect

def signin_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            return redirect("signin")
    return wrapper

def employer_signin(func):
    def wrapper(request,*args,**kwargs):
        if request.user.role=="employer":
            return func(request,*args,**kwargs)
        else:
            return redirect("signin")
    return wrapper

def jobseeker_signin(func):
    def wrapper(request,*args,**kwargs):
        if request.user.role=="jobseeker":
            return func(request,*args,**kwargs)
        else:
            return redirect("signin")
    return wrapper
