"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from tasks import views
from django.contrib.auth.decorators import login_required
from tasks.models import LikeDislike
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
app_name = 'ajax'
urlpatterns = [
    path('', views.Main, name='Main'),
    path('Main/', views.Main, name='Main'),
    path('Register/', views.Register, name='Register'),
    path('Registration/', views.Registration, name='Registration'),
    path('LogInFunc/', views.LogInFunc, name='LogInFunc'),
    path('LogIn/', views.LogIn, name='LogIn'),        
    path('Help/', views.Help, name='Help'),
    path('AddOtzyv/', views.AddOtzyv, name='AddOtzyv'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('rating', views.RatingCreateView.as_view(), name='rating'),
    path('upload-rating', views.UploatRating, name='upload-rating'),
]

urlpatterns += [
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)