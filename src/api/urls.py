"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from resources.views import UnicornViewSet


router = DefaultRouter()
router.register('resource', UnicornViewSet, basename ='Resource')

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentication -- OAuth API
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    #path('openid/', include('oidc_provider.urls', namespace='oidc_provider')),
    path('authentication/', include('users.urls')),
    #path('accounts/login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    path('accounts/', include('django.contrib.auth.urls')),
    # API -- Resource Server
    path('v1/', include(router.urls)),
    path('', include('social_django.urls', namespace='social')),
]
