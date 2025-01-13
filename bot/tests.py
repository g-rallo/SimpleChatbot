from django.test import TestCase
from bot.models import User, Food, FoodCategory


class UserModelTests(TestCase):
    def test_right_nutrition_type_calculated(self):
        """"
        Test if the nutrition type of some users is well calculated given their top 3 favorite foods
        """
        # Creating and saving FoodCategory objects
        vegan_category = FoodCategory(name="Vegan")
        vegetarian_category = FoodCategory(name="Vegetarian")
        omnivore_category = FoodCategory(name="Omnivore")
        vegan_category.save()
        vegetarian_category.save()
        omnivore_category.save()

        # Creating and saving Food objects
        f1 = Food(name="Rice", category=vegan_category)
        f2 = Food(name="Pork", category=omnivore_category)
        f3 = Food(name="Eggs", category=vegetarian_category)
        f4 = Food(name="Sushi", category=vegetarian_category)
        f5 = Food(name="Pasta", category=vegan_category)
        f1.save()
        f2.save()
        f3.save()
        f4.save()
        f5.save()

        # Creating user1 with name Peter that his favorite 3 foods are Rice, Pork and Pasta, which means that he is Omnivore
        u1 = User(name="Peter")
        u1.save()
        u1.favorite_foods.add(f1, f2, f5)
        u1.save()

        # Creating user2 with name Sarah that his favorite 3 foods are Eggs, Sushi and Pasta, which means that she is Vegetarian
        u2 = User(name="Sarah")
        u2.save()
        u2.favorite_foods.add(f3, f4, f5)
        u2.save()

        self.assertEqual(u1.calculate_nutrition(), "Omnivore")
        self.assertEqual(u2.calculate_nutrition(), "Vegetarian")
