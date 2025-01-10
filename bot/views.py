from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import json

from bot.models import FoodCategory, Food, User, Message
from bot.openAIcalls import *

# ---------------------- PAGES ----------------------

def redirect_view(request):
    """
    View to redirect to another url.
    This view is called when the url is "/bot". So being in "/bot" will redirect you to the given url.
    """
    response = redirect('/bot/simulate/')
    return response


def simulate(request):
    """
    View that renders the page with a button to simulate 100 conversations
    """
    return render(request, "bot/simulate.html")


def user_registration(request):
    """
    View that renders the page where the user register himself/herself by writing his/her name
    """
    return render(request, "bot/register.html")

# TODO
def conversation(request, user_id):
    """
    View that renders the page of the conversation with the chatbot
    """

    # Getting the messages from the user passed as parameter
    messages = list(Message.objects.filter(user__id = user_id))

    return render(request, "bot/chat.html", {"messages" : messages})


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


# ---------------------- ACTIONS ----------------------

def simulate_conversations(request):
    """
    View that simulates N conversations
    """
    # simulate N conversations
    for i in range(3):
        # create a user with a random name
        user_name = generate_random_name_prompt()
        print(user_name)
        user_obj = User.objects.create(name=user_name)

        # obtaining and storing question about his/her top 3 favorite foods question
        favorite_foods_question = favorite_food_question_prompt(name=user_name)
        print(favorite_foods_question)
        Message.objects.create(user=user_obj, conversation_stage=Message.CONVERSATION_QUESTIONS["2"], owner=Message.OWNER["BOT"], message=favorite_foods_question)

        # obtaining and storing user answer
        user_answer = favorite_food_answer_prompt()
        print(user_answer)
        Message.objects.create(user=user_obj, conversation_stage=Message.CONVERSATION_QUESTIONS["2"], owner=Message.OWNER["USR"], message=user_answer)

        # identify and storing foods in user answer
        foods_json = identify_food_prompt(message=user_answer)
        print(foods_json)
        for food in json.loads(foods_json)["foods"]:
            food_obj, created = Food.objects.get_or_create(name=food)
            if created:
                category = identify_food_category_prompt(food=food_obj.name)
                print(food_obj, category)
                food_obj.category = FoodCategory.objects.get(name=category)
                food_obj.save()

            # Adding the Food object in the ManyToMany field
            user_obj.favorite_foods.add(food_obj)
        
        # Calculating the nutrition category of the user based on his/her top 3 favorite foods
        user_obj.calculate_nutrition()
        user_obj.save()

    return HttpResponseRedirect(reverse("bot:users"))


def start_conversation(request, name):
    """
    View that initiates a conversation: 
        1. creates a user
        2. creates the first message
    It is called when the button in the user_registration is pressed
    """
    # create a user
    user = User.objects.create(name=name)

    # obtaining and storing question about the user top 3 favorite foods question
    favorite_foods_question = favorite_food_question_prompt(name=user.name)
    Message.objects.create(user=user, conversation_stage=Message.CONVERSATION_QUESTIONS["2"], owner=Message.OWNER["BOT"], message=favorite_foods_question)

    return HttpResponseRedirect(reverse("bot:conversation", args=(user.id,)))

# TODO
def response(request):
    """
    
    """
    return 0
