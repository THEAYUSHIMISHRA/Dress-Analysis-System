from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # rename if needed
    path('dashboard/', views.dashboard, name='dashboard'),  # ✅ dashboard path
    path('logout/', views.logout_view, name='logout'),
]
