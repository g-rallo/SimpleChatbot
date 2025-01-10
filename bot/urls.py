from django.urls import path

from . import views

app_name = "bot"
urlpatterns = [

    # ---------------------- PAGES ----------------------
    # ex: /bot
    path("", views.redirect_view),

    # ex: /bot/simulate
    path("simulate/", views.simulate, name="simulate"),

    # ex: /bot/register
    path("register/", views.user_registration, name="user_registration"),
    # ex: /bot/chat
    path("chat/<int:user_id>/", views.conversation, name="conversation"),

    # ex: /bot/users
    path("users/", views.users, name="users"),
    # ex: /bot/users/5
    path("users/<int:user_id>/", views.user_details, name="user_details"),

    # ---------------------- ACTIONS ----------------------
    
    # ex: /bot/simulate_conversations
    path("simulate_conversations/", views.simulate_conversations, name="simulate_conversations"),
    
    # ex: /bot/create_user
    path("start_conversation/<str:name>/", views.start_conversation, name="start_conversation"),
    # TODO
    # ex: /bot/response
    path("response/", views.response, name="response"),
    
]