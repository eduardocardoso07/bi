# urls.py

from django.contrib import admin
from django.urls import path
from sistem.views import login_view, relatorios_view, logout_view



urlpatterns = [
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('relatorios/', relatorios_view, name='relatorios'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),

]
