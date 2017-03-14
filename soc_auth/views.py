from django.shortcuts import render,redirect,HttpResponseRedirect
from models import Authors
from django.contrib.auth import logout
# Create your views here.

def login_view(request):
    template_name = "auth/login.html"
    if request.user.is_authenticated():
        return HttpResponseRedirect("/wall")
    else:
        return render(request,template_name)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/wall")

def save_profile(backend, user, response,*args, **kwargs):
    obj, created = Authors.objects.get_or_create(user=user)
    print(response)
    if backend.name == 'twitter':
        if 'profile_image_url' in response:
            obj.photo = response['profile_image_url']
    if backend.name == 'google-oauth2':
        if 'image' in response:
            obj.photo = response['image']['url']
    obj.save()


