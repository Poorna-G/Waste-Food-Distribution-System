from django.shortcuts import redirect


def donor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.userprofile.role == 'donor':
            return view_func(request, *args, **kwargs)
        return redirect('home')
    return wrapper


def volunteer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.userprofile.role == 'volunteer':
            return view_func(request, *args, **kwargs)
        return redirect('home')
    return wrapper