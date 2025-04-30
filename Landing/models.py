from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # New field to track read status

    def __str__(self):
        return self.name
    
from django.db import models

class Recipe(models.Model):
    CATEGORY_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snacks', 'Snacks'),
        ('Desserts', 'Desserts'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Recipe Name")
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, verbose_name="Category"
    )
    cuisine = models.CharField(max_length=100, verbose_name="Cuisine Type")
    prep_time = models.PositiveIntegerField(verbose_name="Preparation Time (minutes)")
    cook_time = models.PositiveIntegerField(verbose_name="Cooking Time (minutes)")
    servings = models.PositiveIntegerField(verbose_name="Number of Servings")
    ingredients = models.TextField(verbose_name="List of Ingredients")
    steps = models.TextField(verbose_name="Preparation Steps")
    calories = models.PositiveIntegerField(verbose_name="Calories per Serving")
    carbs = models.PositiveIntegerField(verbose_name="Carbohydrates (grams)")
    protein = models.PositiveIntegerField(verbose_name="Protein (grams)")
    fat = models.PositiveIntegerField(verbose_name="Fat (grams)")
    tags = models.CharField(
        max_length=255, blank=True, verbose_name="Tags (comma-separated)"
    )
    image = models.ImageField(
        upload_to='recipe_images/', blank=True, null=True, verbose_name="Recipe Image"
    )  # Add an image field

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ['name']  # Recipes will be ordered alphabetically by name


from django.db import models
from multiselectfield import MultiSelectField

class MealPlan(models.Model):
    MEAL_TYPE_CHOICES = [
        ('Vegetarian', 'Vegetarian'),
        ('Vegan', 'Vegan'),
        ('High Protein', 'High Protein'),
        ('Low Carb', 'Low Carb'),
        ('Balanced', 'Balanced')
    ]

    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ]

    meal_plan_title = models.CharField(max_length=255)
    description = models.TextField()
    meal_type = models.CharField(max_length=50, choices=MEAL_TYPE_CHOICES)
    days = MultiSelectField(choices=DAYS_OF_WEEK)
    recipes = models.ManyToManyField('Recipe')
    calories_goal = models.IntegerField(null=True, blank=True)
    protein_goal = models.IntegerField(null=True, blank=True)
    carbs_goal = models.IntegerField(null=True, blank=True)
    fat_goal = models.IntegerField(null=True, blank=True)
    meal_plan_image = models.ImageField(upload_to='meal_plan_images/', null=True, blank=True)

    def __str__(self):
        return self.meal_plan_title

from django.db import models

class Content(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('Article', 'Article'),
        ('Video', 'Video'),
        ('Guide', 'Guide'),
        ('Infographic', 'Infographic'),
        ('Other', 'Other'),
    ]

    TOPIC_CATEGORY_CHOICES = [
        ('Nutrition', 'Nutrition'),
        ('Meal Planning', 'Meal Planning'),
        ('Fitness', 'Fitness'),
        ('Mental Health', 'Mental Health'),
        ('Wellness', 'Wellness'),
    ]

    TAG_CHOICES = [
        ('Macronutrients', 'Macronutrients'),
        ('Micronutrients', 'Micronutrients'),
    ]

    content_title = models.CharField(max_length=255)
    description = models.TextField()
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)
    topic_category = models.CharField(max_length=50, choices=TOPIC_CATEGORY_CHOICES)
    upload_file = models.FileField(upload_to='uploads/', blank=True, null=True)
    content_link = models.URLField(blank=True, null=True)
    tags = models.CharField(max_length=20, choices=TAG_CHOICES, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content_title

from django.db import models
from django.contrib.auth.models import User
from datetime import date

class HealthGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_weight = models.FloatField()
    goal_weight = models.FloatField()
    current_calories = models.IntegerField()
    goal_calories = models.IntegerField()
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def has_active_goal(self):
        return self.target_date >= date.today()


# client/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"