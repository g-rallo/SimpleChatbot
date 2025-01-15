# This file registers the app modules in the Django Admin page
from django.contrib import admin
from django.utils.safestring import mark_safe
from bot.models import FoodCategory, Food, User, Message

admin.site.register(FoodCategory)

admin.site.register(Food)

# Customizable admin model class to add more information than the provided by default by Django
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_favorite_foods', 'nutrition']
    search_fields = ["name"] # allows to search for users by their name
    list_filter = ["nutrition"] # allows to filter the users by their nutrition type

    # we need to create a get_favorite_foods function because the favorite_foods attribute is a many to many field and the items in list display have to be strings
    def get_favorite_foods(self, obj):
        return mark_safe(", ".join([child.name for child in obj.favorite_foods.all()]))
    get_favorite_foods.short_description = 'Favorite foods'  #Renames column header
admin.site.register(User, UserAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_owner', 'message']

    # we need to create a get_owner function because the owner attribute string is not displayed be default
    def get_owner(self, obj):
        return obj.owner
    get_owner.short_description = 'Owner'  #Renames column header
admin.site.register(Message, MessageAdmin)