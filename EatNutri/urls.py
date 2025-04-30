"""
URL configuration for EatNutri project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Landing.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',landing_page,name='landing'),
    path('ContactUs/',contact_page,name='contact_page'),
    path('register_user/',register,name='register_user'),
    path('user_login/',user_login,name='user_login'),
    path('admin_login/',admin_login,name='admin_login'),
    path('admin_home/',admin_home,name='admin_home'),
    path('users_registered/',admin_users_registered,name='admin_users_registered'),
    path('admin_users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('admin_add_recipe/', admin_add_recipe, name='admin_add_recipe'),
    path('admin_list_recipes/', admin_list_recipes, name='admin_list_recipes'),
    path('admin_view_recipe/<int:recipe_id>/', admin_view_recipe, name='admin_view_recipe'),
    path('admin_edit_recipe/<int:recipe_id>/', admin_edit_recipe, name='admin_edit_recipe'),
    path('admin_delete_recipe/<int:recipe_id>/', admin_delete_recipe, name='admin_delete_recipe'),
    path('admin_add_mealplan/',admin_add_mealplan,name='admin_add_mealplan'),
    path('admin_record_mealplan/',admin_record_mealplan,name='admin_record_mealplan'),
    path('meal-plan/<int:meal_plan_id>/view/', view_meal_plan, name='view_meal_plan'),
    path('meal-plan/<int:meal_plan_id>/edit/', edit_meal_plan, name='edit_meal_plan'),
    path('meal-plan/<int:meal_plan_id>/delete/', delete_meal_plan, name='delete_meal_plan'),
    path('admin_upload_educontent/', admin_upload_educontent, name='admin_upload_educontent'),
    path('admin_record_educontent/', admin_record_educontent, name='admin_record_educontent'),
    path('admin_view_educontent/<int:pk>/', admin_view_educontent, name='admin_view_educontent'),  # View content
    path('admin_edit_educontent/<int:pk>/edit/',admin_edit_educontent, name='admin_edit_educontent'),  # Edit content
    path('admin_delete_educontent/<int:pk>/delete/',admin_delete_educontent, name='admin_delete_educontent'),  # Delete content
    path('admin_contact_list/', admin_contact_list, name='admin_contact_list'),
    path('admin_mark_as_read/<int:pk>/', admin_mark_as_read, name='admin_mark_as_read'),
    path('admin_logout/',admin_logout,name='admin_logout'),


    path('client_dashboard/', client_dashboard, name='client_dashboard'),
    path('client_meal_plan_list/', client_meal_plan_list, name='client_meal_plan_list'),
    path('client_meal_plan_detail/<int:pk>/', client_meal_plan_detail, name='client_meal_plan_detail'),
    path('client_recipe_list/',client_recipe_list,name='client_recipe_list'),
    path('client_recipe_detail/<int:pk>/', client_recipe_detail, name='client_recipe_detail'),
    path('client_educontent_list/',client_educontent_list,name='client_educontent_list'),
    path('client_educontent_detail/<int:content_id>/',client_educontent_detail,name='client_educontent_detail'),

    path('client_logout/',client_logout,name='client_logout'),
    path('client_records/',client_records,name='client_records'),

    path('client_bodymetric_view/',client_bodymetric_view,name='client_bodymetric_view'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)