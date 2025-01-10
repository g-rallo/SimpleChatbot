from django.core.management.base import BaseCommand
from bot.models import FoodCategory


class Command(BaseCommand):
    help = "This command is executed at the start when the docker container is build. It creates a set of given Food Categories (nutrition types)"

    # FoodCategories objects to be created when the app is build
    food_categories = ["Omnivore", "Vegetarian", "Vegan"]

    def handle(self, *args, **options):
        
        for element in self.food_categories:
            FoodCategory.objects.get_or_create(name=element)
