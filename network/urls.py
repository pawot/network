
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_post', views.create_post, name="create_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("change_follow", views.change_follow, name="change_follow"),
    path("following", views.following, name="following"),
    path("update_post/<int:post_id>", views.update_post, name="update_post"),
    path("like_post/<int:post_id>/<str:type>", views.like_post, name="like_post"),
]
