from django.shortcuts import render

# Auth
def admin_login(request):
    return render(request, 'auth/login.html')

def change_password(request):
    return render(request, 'auth/change_password.html')

# Dashboard
def dashboard(request):
    return render(request, 'admin_dashboard.html')

# Movies
def movie_list(request):
    return render(request, 'movies/movie_list.html')

def add_movie(request):
    return render(request, 'movies/add_movie.html')


def view_movie(request):
    return render(request, 'movies/view_details.html')

# Users
def user_list(request):
    return render(request, 'users/users_list.html')

def user_history(request):
    return render(request, 'users/view_history.html')

# Reports
def report(request):
    return render(request, 'report.html')