# This file registers the app modules in the Django Admin page
from django.contrib import admin
from django.utils.safestring import mark_safe
from bot.models import FoodCategory, Food, User

admin.site.register(FoodCategory)

admin.site.register(Food)

# Customizable admin model class to add more information than the provided by default by Django
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_favorite_foods', 'nutrition']

    # we need to create a get_favorite_foods function because the favorite_foods attribute is a many to many field and the items in list display have to be strings
    def get_favorite_foods(self, obj):
        return mark_safe(", ".join([child.name for child in obj.favorite_foods.all()]))
    get_favorite_foods.short_description = 'Favorite foods'  #Renames column header
admin.site.register(User, UserAdmin)
