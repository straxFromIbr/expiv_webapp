from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("account", views.account, name="account"),
    path("auth", views.auth, name="auth"),
    # path("login", views.login, name="login"),
]
