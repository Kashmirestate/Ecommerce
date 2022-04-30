from django.shortcuts import redirect

def decorator(func):
    def inner(request,*args,**kwargs):
        if request.session.get('check'):
            return func(request,*args,**kwargs)
        else:
            return redirect('login_page')
    return inner