from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.http import HttpResponse

from bot.models import FoodCategory, Food, User

def redirect_view(request):
    """
    View to redirect to another url.
    This view is called when the url is "/bot". So being in "/bot" will redirect you to "/bot/users/"
    """
    response = redirect('/bot/users/')
    return response

def users(request):
    """
    View that shows a list of all the users
    """
    current_users = User.objects.all()
    context = {
        "current_users": current_users,
    }
    return render(request, "bot/users.html", context)


def user_details(request, user_id):
    """
    View that shows the details of a certain user
    """
    user = get_object_or_404(User, pk=user_id)
    return render(request, "bot/user_details.html", {"user": user})
