# This file contains all the database models of the app 
from django.db import models

class FoodCategory(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        constraints = [
            # We don't allow multiple FoodCategory objects with the same name
            models.UniqueConstraint(fields=["name"], name="unique Food Category")
        ]

    def __str__(self):
        return self.name
    
class Food(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(FoodCategory, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            # We don't allow multiple Food objects with the same name
            models.UniqueConstraint(fields=["name"], name="unique Food")
        ]
    
    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=200)
    favorite_foods = models.ManyToManyField(Food, blank=True, related_name="liked_by")
    nutrition = models.ForeignKey(FoodCategory, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def calculate_nutrition(self):
        """
        Calculates the nutrition category from the user based on his/her top 3 favorite foods
        """
        # If he/she likes a food that only Omnivore people can eat -> he/she will be Omnivore
        if len([food for food in list(self.favorite_foods.all()) if food.category.name == "Omnivore"]):
            self.nutrition, _ = FoodCategory.objects.get_or_create(name="Omnivore")

        # If the previous one is not true and he/she likes a food that only Vegetarian people can eat -> he/she will be Vegetarian
        elif len([food for food in list(self.favorite_foods.all()) if food.category.name == "Vegetarian"]):
            self.nutrition, _ = FoodCategory.objects.get_or_create(name="Vegetarian")

        # Otherwise he/she only likes food that Vegan people can eat -> so he/she will be vegetarian
        else:
            self.nutrition, _ = FoodCategory.objects.get_or_create(name="Vegan")
        
        return self.nutrition.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Stages/questions of the conversation
    CONVERSATION_QUESTIONS = {
        "1" : "NAME",
        "2" : "FOOD",
        "3" : "FINISH"
    }
    conversation_stage = models.CharField(max_length=4, choices=CONVERSATION_QUESTIONS)

    # Owner of the message
    OWNER = {
        "USR" : "User",
        "BOT" : "Bot"
    }
    owner = models.CharField(max_length=4, choices=OWNER)

    message = models.CharField(max_length=200)

    def __str__(self):
        return self.message
