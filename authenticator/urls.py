from django.urls import path
from . import views
from django.contrib.auth import views as auth
urlpatterns = [
    path('login/', views.mylogin, name="login"),
    path('register/', views.myregister, name="register"),
    path('logout/', auth.LogoutView.as_view(next_page="home"), name="logout"),
]
