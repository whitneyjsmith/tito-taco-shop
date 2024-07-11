"""tito-taco-shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import django_cas_ng.views
from rest_framework.routers import DefaultRouter
from . import views
from user.views import MEView
from products.views import ProductViewset
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

api_router = DefaultRouter()
api_router.register(r'products', ProductViewset, basename='products')

urlpatterns = [
    path('user/me/', MEView.as_view(), name='me'),
    path('account/login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('account/logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('admin/', admin.site.urls),
    # path('slack/', include('django_slack_oauth.urls')),
    path('integration/', include('integration.urls')),
    path('', views.index, name='home-page'),
    path('products/', include('products.urls')),
    path('api/v1/', include(api_router.urls)),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]