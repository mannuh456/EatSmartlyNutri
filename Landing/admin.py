from django.contrib import admin
from .models import Contact,Recipe,MealPlan,Content,HealthGoal
# Register your models here.

admin.site.register(Contact)
admin.site.register(Recipe)
admin.site.register(MealPlan)
admin.site.register(Content)
admin.site.register(HealthGoal)