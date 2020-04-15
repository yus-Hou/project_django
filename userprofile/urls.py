from django.urls import path
from . import views

app_name = 'userprofile'
urlpatterns = [
    path('login/', views.user_login, name= 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('register/', views.user_register, name = 'register'),
    path('check_name', views.check_name, name = "check_name"),
    path('check_email', views.check_email, name = 'check_email'),
    path('check_phone', views.check_phone, name = 'check_phone'),
    path('edit/<int:id>/', views.profile_edit, name = 'edit'),
    path('userpage/<int:id>', views.personal_center, name = "userpage"),


]