from django.urls import path

from . import views

app_name = "bot"
urlpatterns = [
    path("", views.redirect_view),
    # ex: /bot/users
    path("users/", views.users, name="users"),
    # ex: /bot/users/5
    path("users/<int:user_id>/", views.user_details, name="user_details"),

]