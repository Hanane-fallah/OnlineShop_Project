from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """
    this function restricts view for authenticated users
    :param view_func: template view
    :return: to landing if user is authenticated
    :else: run view_func
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def admin_user(view_func):
    """
    this function restricts some views for admin user
    :param view_func: template view
    :return: to admin panel if user is admin
    :else:  run view_func
    """
    def wrapper_func(request, *args, **kwargs):
        # users with is_staff == True can access admin panel
        if request.user.is_staff == True:
            return redirect('admin:login')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
