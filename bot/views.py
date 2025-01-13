# This file contains all the views from the bot Django app
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


def simulate_conversations(request):
    """
    View that renders the page with a button to simulate 100 conversations
    """
    return render(request, "bot/simulate.html")


def user_registration(request):
    """
    View that renders the page where the user register himself/herself by writing his/her name
    """
    return render(request, "bot/register.html")


def conversation(request, user_id):
    """
    View that renders the page of the conversation with the chatbot.
    Obtains all the messages form the user with the id sent as a parameter and they will be displayed in the page.
    """

    # Getting the messages from the user passed as parameter
    messages = list(Message.objects.filter(user__id = user_id))

    return render(request, "bot/chat.html", {"user_id" : user_id, "messages" : messages})

class UsersView(generic.ListView):
    template_name = "bot/users.html"
    context_object_name = "current_users"

    def get_queryset(self):
        """Return the last five published questions."""
        return User.objects.all()


def nutrition_users(request, nutrition):
    """
    View that shows a list of all the users with a the nutrition given as a parameter
    """
    current_users = User.objects.filter(nutrition__name=nutrition)
    context = {
        "current_users": current_users,
        "nutrition": nutrition,
    }
    return render(request, "bot/users.html", context)

class DetailView(generic.DetailView):
    """
    Default django view that shows the details of a user
    """
    model = User
    template_name = "bot/user_details.html"


# ---------------------- ACTIONS ----------------------

def simulate_conversations(request):
    """
    View that simulates N conversations
    """
    # simulate N conversations
    for i in range(3):
        # create a user with a random name
        user_name = generate_random_name_prompt()

        user_obj = User.objects.create(name=user_name)

        # obtaining and storing question about his/her top 3 favorite foods question
        favorite_foods_question = favorite_food_question_prompt(name=user_name)
        Message.objects.create(user=user_obj, conversation_stage=Message.CONVERSATION_QUESTIONS["2"], owner=Message.OWNER["BOT"], message=favorite_foods_question)

        # obtaining and storing user answer
        user_answer = favorite_food_answer_prompt()
        Message.objects.create(user=user_obj, conversation_stage=Message.CONVERSATION_QUESTIONS["2"], owner=Message.OWNER["USR"], message=user_answer)

        # identify and storing foods in user answer
        foods_json = identify_food_prompt(message=user_answer)
        for food in json.loads(foods_json)["foods"]:
            food_obj, created = Food.objects.get_or_create(name=food)

            # it could be that the food had already been mentioned before by another user, in that case we already have its category
            if created:
                category = identify_food_category_prompt(food=food_obj.name)
                food_obj.category = FoodCategory.objects.get(name=category)
                food_obj.save()

            # Adding the Food as a favorite one of the user (adding object in the ManyToMany field)
            user_obj.favorite_foods.add(food_obj)
        
        # Calculating the nutrition category of the user based on his/her top 3 favorite foods
        user_obj.calculate_nutrition()
        user_obj.save()

    return HttpResponseRedirect(reverse("bot:users"))


def start_conversation(request):
    """
    View that initiates a conversation: 
        1. creates a user
        2. creates the first question from the bot
    It is called when the button in the user_registration is pressed
    """
    # we get the userName from the form input divs, using the name parameter values to access them
    user_name = request.POST['userName']

    # create a user
    user = User.objects.create(name=user_name)

    # obtaining and storing question about the user top 3 favorite foods question
    favorite_foods_question = favorite_food_question_prompt(name=user.name)
    Message.objects.create(user=user, conversation_stage=Message.CONVERSATION_QUESTIONS["2"], owner=Message.OWNER["BOT"], message=favorite_foods_question)

    return HttpResponseRedirect(reverse("bot:conversation", args=(user.id,)))


def response(request, user_id):
    """
    View that processes the user message and gives and answer
        1. Gets the user message from the POST dictionary
        2. Creates a Message object to store the message
        3. Identify the foods mentioned in the message
        4. Creates a Food object and obtains its category if the food hadn't been mentioned before by another user
        5. Adds the food to the favorite foods of the user
        6. Calculates the user nutrition type
        7. Stores a message with the answer from the bot

    It is called when the user sends a message
    """

    # we get the message from the form input divs, using the name parameter values to access them
    use_message = request.POST['message']
    user = User.objects.get(pk=user_id)

    Message.objects.create(user=user, conversation_stage=Message.CONVERSATION_QUESTIONS["2"], owner=Message.OWNER["USR"], message=use_message)

    # identify and storing foods in user answer
    foods_json = identify_food_prompt(message=use_message)

    for food in json.loads(foods_json)["foods"]:
        food_obj, created = Food.objects.get_or_create(name=food)
        if created:
            category = identify_food_category_prompt(food=food_obj.name)

            food_obj.category = FoodCategory.objects.get(name=category)
            food_obj.save()

        # Adding the Food object in the ManyToMany field
        user.favorite_foods.add(food_obj)
    
    # Calculating the nutrition category of the user based on his/her top 3 favorite foods
    user.calculate_nutrition()
    user.save()

    bot_answer = f"It looks like you are {user.nutrition}!"
    Message.objects.create(user=user, conversation_stage=Message.CONVERSATION_QUESTIONS["2"], owner=Message.OWNER["BOT"], message=bot_answer)

    return HttpResponseRedirect(reverse("bot:conversation", args=(user.id,)))
