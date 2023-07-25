from django.urls import path
from django.conf.urls import include
from . import views
urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('success', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('qr_code/<int:pk>/', views.generate_qr, name='generate_qr')
]