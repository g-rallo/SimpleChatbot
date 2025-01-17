from multiprocessing import Process
from datetime import datetime
from django.core.management.base import BaseCommand
import json

from bot.models import FoodCategory, Food, User, Message
from bot.openAIcalls import *


class Command(BaseCommand):
    help = """
        This command is to simulate a certain number of conversations with different users at the same time. 
        You can choose the number of conversations to be executed (--n parameter) and the way of execution (--execution parameter[serial/parallel]).
        
        
        Ex: the following command will simulate 10 conversations in parallel.
            python manage.py --n 10 -e p

            p: parallel
            s: serial
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--n',
            dest='n',
            type=int,
            default=100,
            help='Name of conversations to be simulated',
        )

        parser.add_argument(
            '--execution',
            dest='e',
            type=str,
            default='s',
            help='Type of execution of the conversations (serial/parallel)',
        )
    
    def simulate_conversation(self):
        # create a user with a random name
        user_name = generate_random_name_prompt()

        user_obj = User.objects.create(name=user_name)

        # obtaining and storing question about his/her top 3 favorite foods question
        favorite_foods_question = favorite_food_question_prompt(name=user_name)
        Message.objects.create(user=user_obj, conversation_stage=Message.CONVERSATION_QUESTIONS["2"], owner=Message.OWNER["BOT"], message=favorite_foods_question[:200])

        # obtaining and storing user answer
        user_answer = favorite_food_answer_prompt()
        Message.objects.create(user=user_obj, conversation_stage=Message.CONVERSATION_QUESTIONS["2"], owner=Message.OWNER["USR"], message=user_answer[:200])

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


    def handle(self, *args, **options):
        """
        Executes n number of conversations with different users in serial or parallel.
        These 2 attributes are given as parameters:
            --n <int:number of conversations>
            --execution <str:p(parallel)/s(serial)>

        """
        execution = options['e']
        n_conversations = options['n']
        start = datetime.now()

        if execution == 's':
            # Serial execution
            for i in range(n_conversations):
                print(f"Running conversation {i+1}")
                self.simulate_conversation()
        
        elif execution == 'p':
            # Parallel execution
            proc = []
            for i in range(n_conversations):
                print(f"Starting conversation {i+1}")  
                p = Process(target=self.simulate_conversation())
                p.start()
                proc.append(p)

            for p in proc:
                p.join()
        
        finish = datetime.now()

        print(f"Executed in {finish-start}")
