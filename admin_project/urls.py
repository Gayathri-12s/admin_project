"""
URL configuration for admin_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include


from admin_app import views

urlpatterns = [
    
     path('', views.admin_login, name='home'),
   
    path('admin/', admin.site.urls),
    

   # Auth
    path("login/", views.admin_login, name='login'),
    path('change-password/', views.change_password, name='change_password'),
    path("logout/", views.admin_logout, name="logout"),



    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Movies
   # Movies

path('movies/', views.movie_list, name='movie_list'),
path('movies/add/', views.add_movie, name='add_movie'),
path('movies/edit/<int:id>/', views.edit_movie, name='edit_movie'),
path('movies/delete/<int:id>/', views.delete_movie, name='delete_movie'),
path('movies/view/<int:id>/', views.view_movie, name='view_movie'),

    # Users
    path('users/', views.user_list, name='user_list'),
    path("users/block/<int:id>/", views.block_user, name="block_user"),
    path("users/unblock/<int:id>/", views.unblock_user, name="unblock_user"),
    path("users/delete/<int:id>/", views.delete_user, name="delete_user"),
    path("users/history/<int:id>/", views.user_history, name="user_history"),
    
    path('reports/', views.report, name='report'),
    
    
     path('api/', include(('user_api.urls', 'api'), namespace='api')),
    
]
