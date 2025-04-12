from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False)),  # 添加根路径重定向
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # 修改路径
    path('chat/', include('chat.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
