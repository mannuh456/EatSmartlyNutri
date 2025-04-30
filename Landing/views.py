from django.shortcuts import render

# management_index
def landing_page(request):
    template = 'index.html'
    return render(request, template)




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        Contact.objects.create(name=name, email=email, subject=subject, message=message)

        # Show a success message
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact_page')

    return render(request, 'contact.html')


from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set the password using the hashed value
            user.save()

            # Log the user in
            login(request, user)

            return redirect('landing')  # Redirect to the login page or another page

    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('client_dashboard')  # Redirect to home page or a dashboard

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:  # Check if the user is a superadmin
                login(request, user)
                return redirect('admin_home')  # Replace 'admin_dashboard' with your superadmin dashboard URL name
            else:
                messages.error(request, "Access denied: Only superadmins can log in here.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'admin_login.html', {'form': form})

# management_index
def admin_home(request):
    total_users = User.objects.count()  # Total number of registered users
    active_users = User.objects.filter(is_active=True).count()  # Number of active users
    context = {
            'total_users': total_users,
            'active_users': active_users,
    }
    template = 'admin_landing.html'
    return render(request, template, context)


# management_index
def admin_users_registered(request):
    users = User.objects.filter(is_superuser=False)
    context = {
        'users': users,
    }
    template = 'admin_users_registered.html'
    return render(request, template,context)

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        return HttpResponseForbidden("You cannot delete a superadmin.")
    
    user.delete()
    return redirect('admin_users_registered')  # Redirect back to the user list

from django.shortcuts import render, redirect
from .forms import RecipeForm

def admin_add_recipe(request):
    template = 'admin_add_recipe.html'

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)  # Include request.FILES for file uploads if necessary
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('admin_add_recipe')  # Redirect to avoid re-submission
        else:
            print(form.errors)  # Debugging: Print errors in case the form isn't valid
    else:
        form = RecipeForm()

    return render(request, template, {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe
from .forms import RecipeForm
from django.contrib import messages

def admin_list_recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'admin_record_recipe.html', {'recipes': recipes})

def admin_view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'admin_view_recipe.html', {'recipe': recipe})

def admin_edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, "Recipe updated successfully.")
            return redirect('admin_list_recipes')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'admin_add_recipe.html', {'form': form, 'recipe': recipe})

def admin_delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, "Recipe deleted successfully.")
        return redirect('admin_list_recipes')
    return render(request, 'admin_delete_recipe.html', {'recipe': recipe})


from django.shortcuts import render, redirect
from .forms import MealPlanForm
from .models import Recipe

def admin_add_mealplan(request):
    recipes = Recipe.objects.all()
    if request.method == 'POST':
        form = MealPlanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_add_mealplan')  # Replace with a success page
    else:
        form = MealPlanForm()
    return render(request, 'admin_add_mealplan.html', {'form': form, 'recipes': recipes})

from django.shortcuts import render
from .models import MealPlan

def admin_record_mealplan(request):
    meal_plans = MealPlan.objects.prefetch_related('recipes').all()
    return render(request, 'admin_record_mealplan.html', {'meal_plans': meal_plans})


from django.shortcuts import get_object_or_404, render
from .models import MealPlan

def view_meal_plan(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id)
    return render(request, 'admin_view_mealplan.html', {'meal_plan': meal_plan})


from django.shortcuts import redirect
from .forms import MealPlanForm

def edit_meal_plan(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id)
    if request.method == 'POST':
        form = MealPlanForm(request.POST, request.FILES, instance=meal_plan)
        if form.is_valid():
            form.save()
            return redirect('admin_add_mealplan')
    else:
        form = MealPlanForm(instance=meal_plan)
    return render(request, 'admin_add_mealplan.html', {'form': form})

def delete_meal_plan(request, meal_plan_id):
    meal_plan = get_object_or_404(MealPlan, id=meal_plan_id)
    if request.method == 'POST':
        meal_plan.delete()
        return redirect('admin_record_mealplan')
    return render(request, 'confirm_delete.html', {'meal_plan': meal_plan})



from django.shortcuts import render, redirect
from .forms import ContentForm
from django.contrib import messages

def admin_upload_educontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # This will save the data to the database
            messages.success(request, 'Content uploaded successfully!')
            return redirect('admin_record_educontent')  # Replace with your desired redirect view
        else:
            messages.error(request, 'There was an error with your submission.')
    else:
        form = ContentForm()
    
    return render(request, 'admin_upload_educontent.html', {'form': form})

from django.shortcuts import render
from .models import Content

def admin_record_educontent(request):
    contents = Content.objects.all()
    return render(request, 'admin_record_educontent.html', {'contents': contents})


from django.shortcuts import get_object_or_404, render
from .models import Content  # Replace with your model name

def admin_view_educontent(request, pk):
    content = get_object_or_404(Content, pk=pk)
    return render(request, 'admin_view_educontent.html', {'content': content})

from django.shortcuts import redirect

def admin_edit_educontent(request, pk):
    content = get_object_or_404(Content, pk=pk)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            return redirect('admin_record_educontent')
    else:
        form = ContentForm(instance=content)
    return render(request, 'admin_upload_educontent.html', {'form': form, 'content': content})

from django.contrib import messages

def admin_delete_educontent(request, pk):
    content = get_object_or_404(Content, pk=pk)
    if request.method == 'POST':
        content.delete()
        messages.success(request, 'Content deleted successfully!')
        return redirect('admin_record_educontent')  # Replace with your list view name
    return render(request, 'admin_record_educontent.html', {'content': content})

from django.shortcuts import get_object_or_404, redirect, render
from .models import Contact

def admin_contact_list(request):
    contacts = Contact.objects.all().order_by('-created_at') 
    return render(request, 'admin_contact_list.html', {'contacts': contacts})

def admin_mark_as_read(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.read = True  # Mark as read
    contact.save()
    return redirect('admin_contact_list')  # Redirect to the contact list

from .models import Profile
from django.core.files.storage import FileSystemStorage
import os
def client_dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'profile_image' in request.FILES:
            # Upload new image
            profile_image = request.FILES['profile_image']
            profile.profile_image = profile_image
            profile.save()
            return redirect('client_dashboard')
        elif 'delete_image' in request.POST:
            # Delete current image
            if profile.profile_image:
                # Remove the file from storage
                if os.path.isfile(profile.profile_image.path):
                    os.remove(profile.profile_image.path)
                profile.profile_image = None
                profile.save()
            return redirect('client_dashboard')

    context = {
        'last_login': request.user.last_login,
        'profile': profile,
    }
    template = 'client_dashboard.html'
    return render(request, template, context)


from django.shortcuts import render
from .models import MealPlan

def client_meal_plan_list(request):
    meal_type_filter = request.GET.get('meal_type')
    day_filter = request.GET.get('day')

    # Filter meal plans based on selected filters
    meal_plans = MealPlan.objects.all()
    if meal_type_filter:
        meal_plans = meal_plans.filter(meal_type=meal_type_filter)
    if day_filter:
        meal_plans = meal_plans.filter(days__icontains=day_filter)

    context = {
        'meal_plans': meal_plans,
        'meal_types': MealPlan.MEAL_TYPE_CHOICES,
        'days': MealPlan.DAYS_OF_WEEK,
    }
    return render(request, 'client_meal_plan_list.html', context)

def client_meal_plan_detail(request, pk):
    meal_plan = MealPlan.objects.get(pk=pk)  # Fetch a single meal plan
    return render(request, 'client_meal_plan_detail.html', {'meal_plan': meal_plan})

from django.shortcuts import render
from .models import Recipe

def client_recipe_list(request):
    category_filter = request.GET.get('category')
    cuisine_filter = request.GET.get('cuisine')
    search_query = request.GET.get('search')

    # Filter recipes based on category, cuisine, and search query
    recipes = Recipe.objects.all()
    if category_filter:
        recipes = recipes.filter(category=category_filter)
    if cuisine_filter:
        recipes = recipes.filter(cuisine__icontains=cuisine_filter)
    if search_query:
        recipes = recipes.filter(name__icontains=search_query)

    context = {
        'recipes': recipes,
        'categories': Recipe.CATEGORY_CHOICES,
    }
    return render(request, 'client_recipe_list.html', context)

def client_recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    related_recipes = Recipe.objects.filter(tags__icontains=recipe.tags).exclude(id=pk)[:4]
    context = {
        'recipe': recipe,
        'related_recipes': related_recipes,
    }
    return render(request, 'client_recipe_detail.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Content

def client_educontent_list(request):
    contents = Content.objects.all()
    content_types = Content.CONTENT_TYPE_CHOICES
    topic_categories = Content.TOPIC_CATEGORY_CHOICES

    # Filtering
    content_type = request.GET.get('content_type')
    topic_category = request.GET.get('topic_category')
    search = request.GET.get('search')

    if content_type:
        contents = contents.filter(content_type=content_type)
    if topic_category:
        contents = contents.filter(topic_category=topic_category)
    if search:
        contents = contents.filter(content_title__icontains=search)

    return render(request, 'client_educontent_list.html', {
        'contents': contents,
        'content_types': content_types,
        'topic_categories': topic_categories
    })

def client_educontent_detail(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    return render(request, 'client_educontent_detail.html', {'content': content})

from django.contrib.auth import logout
from django.shortcuts import redirect

def client_logout(request):
    logout(request)
    return redirect('landing')  # Replace 'home' with the name of your homepage URL pattern.

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def admin_logout(request):
    """Logs out the admin user and redirects to the login page."""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully.")
    return redirect('admin_login')  # Replace 'admin_login' with the name of your login URL pattern



from django.shortcuts import render, redirect
from .models import HealthGoal
from .forms import HealthGoalForm
import json

def client_bodymetric_view(request):
    user = request.user
    goal = HealthGoal.objects.filter(user=user).first()

    # If the goal exists & the target date has not passed → Show Graphs
    if goal and goal.has_active_goal():
        data = {
            "current_weight": goal.current_weight,
            "goal_weight": goal.goal_weight,
            "current_calories": goal.current_calories,
            "goal_calories": goal.goal_calories
        }
        return render(request, "client_bodymetric_chart.html", {"data": json.dumps(data)})

    # Otherwise → Show the Form
    if request.method == "POST":
        form = HealthGoalForm(request.POST, instance=goal)  # Update existing goal if available
        if form.is_valid():
            new_goal = form.save(commit=False)
            new_goal.user = user
            new_goal.save()
            return redirect('client_bodymetric_view')  # Refresh to show the graph
    else:
        form = HealthGoalForm(instance=goal)

    return render(request, "client_bodymetric_form.html", {"form": form})


from django.contrib.auth.views import PasswordResetConfirmView

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'



# client/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HealthGoal

@login_required
def client_records(request):
    # Fetch the HealthGoal for the logged-in user, if it exists
    try:
        health_goal = HealthGoal.objects.get(user=request.user)
    except HealthGoal.DoesNotExist:
        health_goal = None

    context = {
        'health_goal': health_goal,
    }
    return render(request, 'client_records.html', context)