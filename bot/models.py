# This file contains all the database models of the app 
from django.db import models

class FoodCategory(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="unique Food Category")
        ]

    def __str__(self):
        return self.name
    
class Food(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(FoodCategory, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [
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
        if len([food for food in list(self.favorite_foods.all()) if food.category.name == "Omnivore"]):
            self.nutrition, _ = FoodCategory.objects.get_or_create(name="Omnivore")
        elif len([food for food in list(self.favorite_foods.all()) if food.category.name == "Vegetarian"]):
            self.nutrition, _ = FoodCategory.objects.get_or_create(name="Vegetarian")
        else:
            self.nutrition, _ = FoodCategory.objects.get_or_create(name="Vegan")
