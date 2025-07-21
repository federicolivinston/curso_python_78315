def is_admin(request):
    if request.user.is_authenticated:
        return {'is_admin': request.user.groups.filter(name='admin').exists()}
    return {'is_admin': False}
