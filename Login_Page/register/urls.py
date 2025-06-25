from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # For login/logout

urlpatterns = [
    path('', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),

    # Optional: Add login and logout routes
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]
