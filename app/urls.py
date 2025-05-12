# urls.py

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from sistem.views import login_view, logistica_view, logout_view, tela_view, comercial_view, financeiro_view, marketing_view, new_brinde_view, brinde_update_view, brinde_delete_view, lancamento_view, lista_lancamento_view, lancamento_delete_view, exportar_lancamentos_excel
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('tela/', tela_view, name='tela'),
    path('tela/logistica/', logistica_view, name='logistica'),

    path('tela/comercial/', comercial_view, name='comercial'),
    path('tela/financeiro/', financeiro_view, name='financeiro'),
    path('tela/marketing/new_brinde/', new_brinde_view.as_view(), name="new_brinde"),
    path('tela/marketing/update_brinde/<int:pk>/', brinde_update_view.as_view(), name="update_brinde"),
    path('tela/marketing/', marketing_view, name='marketing'),
    path('tela/marketing/brinde_delete/<int:pk>/', brinde_delete_view.as_view(), name='brinde_delete' ),
    path('tela/marketing/lista_lancamento/', lista_lancamento_view.as_view(), name='lista_lancamento'),
    path('tela/marketing/lista_lancamento/new_lancamento/', lancamento_view.as_view(), name="new_lancamento"),
    path('tela/marketing/lista_lancamento/lancamento_delete/', lancamento_delete_view, name='lancamento_delete'),
    path('tela/marketing/lista_lancamento/exportar_lancamentos/', exportar_lancamentos_excel, name='exportar_lancamentos'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
