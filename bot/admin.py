# This file registers the app modules in the Django Admin page
from django.contrib import admin
from django.utils.safestring import mark_safe
from bot.models import FoodCategory, Food, User

admin.site.register(FoodCategory)

admin.site.register(Food)

class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_favorite_foods', 'nutrition']

    def get_favorite_foods(self, obj):
        return mark_safe(", ".join([child.name for child in obj.favorite_foods.all()]))
    get_favorite_foods.short_description = 'Favorite foods'  #Renames column header
admin.site.register(User, UserAdmin)
