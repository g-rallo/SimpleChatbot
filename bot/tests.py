# This file contains all the unit tests. To execute them run: python manage.py test
from django.test import TestCase
from django.urls import reverse

from bot.models import User, Food, FoodCategory

def create_test_data():
    """
    Function that creates some data for testing purposes
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


class UserModelTests(TestCase):
    """
    Class for the methods to test the user model view
    """

    def test_right_nutrition_type_calculated_for_user(self):
        """"
        Test if the nutrition type of some users is well calculated given their top 3 favorite foods
        """

        # The database is reset for each test method, so we need to create the data needed for the tests
        create_test_data()

        # getting the user objects
        u1 = User.objects.get(name="Peter")
        u2 = User.objects.get(name="Sarah")

        # checking if their nutrition type is what it should be based on their top 3 favorite foods
        self.assertEqual(u1.calculate_nutrition(), "Omnivore")
        self.assertEqual(u2.calculate_nutrition(), "Vegetarian")


class UsersViewTest(TestCase):
    """
    Class for the methods to test the users view
    """

    def test_all_users_shown_in_users_view(self):
        """
        Tests if the users view is showing all the users created
        """

        # The database is reset for each test method, so we need to create the data needed for the tests
        create_test_data()

        # getting all the users that have to appear in the view
        current_users = User.objects.all()

        # accessing the users page endpoint
        response = self.client.get(reverse("bot:users"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Peter")
        self.assertContains(response, "Sarah")
        # we need to add either ordered=False or make the response.context["current_users"] a list so that it does the assert correctly
        self.assertQuerySetEqual(list(response.context["current_users"]), current_users)
        # self.assertQuerySetEqual(response.context["current_users"], current_users, ordered=False)
    
    def test_vegetarian_user_shown_in_vegetarian_users_view(self):
        """
        Tests if the /users/vegetarian view is showing the vegetarian users
        """

        # The database is reset for each test method, so we need to create the data needed for the tests
        create_test_data()

        # we calculate the nutrition type of every user, this step could also be added in the create_test_data() function but I left if out to test its output in the test_right_nutrition_type_calculated_for_user()
        for u in User.objects.all():
            u.calculate_nutrition()
            u.save()

        # getting the Vegetarian that have to appear in the view
        vegetarian_users = User.objects.filter(nutrition=FoodCategory.objects.get(name="Vegetarian"))

        # accessing the nutrition_users page endpoint: /users/Vegetarian
        response = self.client.get(reverse("bot:nutrition_users", args=("Vegetarian",)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sarah")
        # we need to add either ordered=False or make the response.context["current_users"] a list so that it does the assert correctly
        # self.assertQuerySetEqual(list(response.context["current_users"]), vegetarian_users)
        self.assertQuerySetEqual(response.context["current_users"], vegetarian_users, ordered=False)


class UserDetailsViewTest(TestCase):
    """
    Class for the methods to test the user details view
    """

    def test_user_info_shown_in_details_view(self):
        """
        Test if the details of a user are shown in its detail view
        """

        # The database is reset for each test method, so we need to create the data needed for the tests
        create_test_data()

        # we calculate the nutrition type of every user, this step could also be added in the create_test_data() function but I left if out to test its output in the test_right_nutrition_type_calculated_for_user()
        for u in User.objects.all():
            u.calculate_nutrition()
            u.save()

        user = User.objects.get(name="Peter")

        # accessing the nutrition_users page endpoint: /users/Vegetarian
        response = self.client.get(reverse("bot:user_details", args=(user.id,)))

        # checking that the name, favorite foods and the nutrition are in the response (type appear in the screen)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Peter")
        self.assertContains(response, "Rice")
        self.assertContains(response, "Pork")
        self.assertContains(response, "Pasta")
        self.assertContains(response, "Omnivore")
        self.assertEqual(response.context["user"], user)