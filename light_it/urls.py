"""light_it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from soc_auth.views import login_view
from django.contrib.auth.views import logout




urlpatterns = [
    url(r'^$',login_view),
    url(r'^admin/', admin.site.urls),
    url(r'^wall/',include('wall.urls')),
    url('^soc/', include('social_django.urls', namespace='social')),
    url('^logout/', logout,{'template_name': 'index.html', 'next_page': '/wall'}, name='sign-out'),
]
