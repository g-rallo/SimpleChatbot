from django.urls import path

from . import views

app_name = "bot"
urlpatterns = [

    # ---------------------- PAGES ----------------------
    # ex: /bot
    path("", views.redirect_view),

    # ex: /bot/simulate
    path("simulate/", views.simulate, name="simulate"),

    # TODO
    # ex: /bot/chat/register
    path("chat/register/", views.user_registration, name="user_registration"),
    # ex: /bot/conversation
    path("chat/conversation/", views.conversation, name="conversation"),

    # ex: /bot/users
    path("users/", views.users, name="users"),
    # ex: /bot/users/5
    path("users/<int:user_id>/", views.user_details, name="user_details"),

    # ---------------------- ACTIONS ----------------------
    
    # ex: /bot/simulate_conversations
    path("simulate_conversations/", views.simulate_conversations, name="simulate_conversations"),
    
    # TODO
    # ex: /bot/create_user
    path("create_user/<str:name>/", views.create_user, name="create_user"),
    # ex: /bot/response
    path("response/", views.response, name="response"),
    
]