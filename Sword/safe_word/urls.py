from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    #path('', views.home_page, name="home-page"),
    path('password_generator/', views.generate, name='generate-page'),
    path('password_generator/', views.generate, name='generate-page'),
    # user account
    path('register/', views.register_page, name="register-page"),
    path('login/', views.login_page, name="login-page"),
    path('logged_out/', views.logged_out_page, name="logged_out-page"),
    # user passwords
    path('all_passwords/', views.all_passwords, name="all-page"),
    path('add_password/', views.add_password, name="add-page"),
    path('search_passwords/', views.search_passwords, name="search-page"),
    path('edit/<str:pk>/', views.edit_post, name="edit"),
    path('delete/<str:pk>/', views.delete, name="delete"),
]