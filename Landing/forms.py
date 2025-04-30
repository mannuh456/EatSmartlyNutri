from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message', 'rows': 6}),
        }
from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        # Use email as username
        user.username = user.email
        user.set_password(self.cleaned_data['password'])  # Set the password securely
        if commit:
            user.save()
        return user

from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'name', 'category','image', 'cuisine', 'prep_time', 'cook_time', 
            'servings', 'ingredients', 'steps', 'calories', 
            'carbs', 'protein', 'fat', 'tags'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the recipe name'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select a category'
            }),
            'cuisine': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'E.g., Italian, Indian'
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Preparation time in minutes'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Cooking time in minutes'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Number of servings'
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'List each ingredient, separated by commas',
                'rows': 4
            }),
            'steps': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Detailed cooking steps (step-by-step)',
                'rows': 6
            }),
            'calories': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Calories per serving'
            }),
            'carbs': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Carbohydrates (grams)'
            }),
            'protein': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Protein (grams)'
            }),
            'fat': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Fat (grams)'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'E.g., Vegetarian, Quick, Spicy'
            }),
        }
from django import forms
from .models import MealPlan

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = [
            'meal_plan_title', 'description', 'meal_type', 'days', 
            'recipes', 'calories_goal', 'protein_goal', 'carbs_goal', 
            'fat_goal', 'meal_plan_image'
        ]
        widgets = {
            'days': forms.CheckboxSelectMultiple,  # Renders as checkboxes
            'recipes': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'meal_plan_title': forms.TextInput(attrs={'class': 'form-control'}),
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'calories_goal': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein_goal': forms.NumberInput(attrs={'class': 'form-control'}),
            'carbs_goal': forms.NumberInput(attrs={'class': 'form-control'}),
            'fat_goal': forms.NumberInput(attrs={'class': 'form-control'}),
            'meal_plan_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import Content

class ContentForm(forms.ModelForm):
    tags = forms.ChoiceField(
        choices=Content.TAG_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'tags',
        }),
        required=False
    )

    class Meta:
        model = Content
        fields = [
            'content_title',
            'description',
            'content_type',
            'topic_category',
            'upload_file',
            'content_link',
            'tags',
            'is_featured',
        ]
        widgets = {
            'content_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter content title',
                'id': 'content_title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Provide a brief description of the content',
                'id': 'description',
            }),
            'content_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'content_type',
            }),
            'topic_category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'topic_category',
            }),
            'upload_file': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'id': 'upload_file',
            }),
            'content_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a link to an external resource (e.g., YouTube, blog)',
                'id': 'content_link',
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'is_featured',
            }),
        }

from django import forms
from .models import HealthGoal

class HealthGoalForm(forms.ModelForm):
    class Meta:
        model = HealthGoal
        fields = ['current_weight', 'goal_weight', 'current_calories', 'goal_calories', 'target_date']
        widgets = {
            'current_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter current weight (kg)'}),
            'goal_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter goal weight (kg)'}),
            'current_calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter current daily calories'}),
            'goal_calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter goal daily calories'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

