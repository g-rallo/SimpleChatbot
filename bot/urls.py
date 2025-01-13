from django.urls import path

from . import views

app_name = "bot"
urlpatterns = [

    # ---------------------- PAGES ----------------------
    # ex: /bot/
    path("", views.redirect_view),

    # ex: /bot/simulate/
    path("simulate/", views.simulate_conversations, name="simulate"),

    # ex: /bot/register/
    path("register/", views.user_registration, name="user_registration"),
    # ex: /bot/chat/5/
    path("chat/<int:user_id>/", views.conversation, name="conversation"),

    # ex: /bot/users/
    path("users/", views.users, name="users"),
    # ex: /bot/users/5/
    path("users/<int:user_id>/", views.user_details, name="user_details"),
    # ex: /bot/users/nutrition/vegetarian/
    path("users/<str:nutrition>/", views.nutrition_users, name="nutrition_users"),

    # ---------------------- ACTIONS ----------------------
    
    # ex: /bot/simulate_conversations/
    path("simulate_conversations/", views.simulate_conversations, name="simulate_conversations"),
    
    # ex: /bot/start_conversation/
    path("start_conversation/", views.start_conversation, name="start_conversation"),

    # ex: /bot/response/5/
    path("response/<int:user_id>/", views.response, name="response"),
    
]