# This file contains all the API endpoints of the bot Django app
from django.urls import path

from . import views

app_name = "bot"
urlpatterns = [

    # ---------------------- PAGES ----------------------
    # ex: /bot/
    path("", views.redirect_view),

    # ex: /bot/register/
    path("register/", views.user_registration, name="user_registration"),
    # ex: /bot/chat/5/
    path("chat/<int:user_id>/", views.conversation, name="conversation"),

    # ex: /bot/users/
    path("users/", views.UsersView.as_view(), name="users"),
    # ex: /bot/users/5/
    # we use pk to use the default Django DetailView
    path("users/<int:pk>/", views.DetailView.as_view(), name="user_details"),
    # ex: /bot/users/vegetarian/
    path("users/<str:nutrition>/", views.nutrition_users, name="nutrition_users"),

    # ex: /bot/users/vegetarian/api/
    path("users/<str:nutrition>/api/", views.UsersNutritionList.as_view(), name="nutrition_users_api"),

    # ---------------------- ACTIONS ----------------------    
    # ex: /bot/start_conversation/
    path("start_conversation/", views.start_conversation, name="start_conversation"),

    # ex: /bot/response/5/
    path("response/<int:user_id>/", views.response, name="response"),
    
]