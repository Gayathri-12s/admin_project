from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from .models import Movie, WatchHistory
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash

    

from .models import User


def admin_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(
                email=email,
                is_admin=True,
                is_active=True
            )

        except User.DoesNotExist:

            messages.error(request, "Invalid email or password")
            return render(request, "auth/login.html")


        # Check password manually
        if not check_password(password, user.password):

            messages.error(request, "Invalid email or password")
            return render(request, "auth/login.html")


        # Login user (important)
        login(request, user)

        return redirect("dashboard")


    return render(request, "auth/login.html")



# ----------------------------------
# Logout
# ----------------------------------
def admin_logout(request):
    logout(request)
    return redirect("login")


# ----------------------------------
# Dashboard
# ----------------------------------
@login_required(login_url="/login/")
def dashboard(request):

    total_movies = Movie.objects.count()
    total_users = User.objects.filter(is_admin=False).count()
    total_views = Movie.objects.aggregate(
        total=Sum("view_count")
    )["total"] or 0

    recent_movies = Movie.objects.all().order_by("-id")[:5]

    return render(request, "admin_dashboard.html", {
        "total_movies": total_movies,
        "total_users": total_users,
        "total_views": total_views,
        "recent_movies": recent_movies,
    })

# ----------------------------------
# Movies
# ----------------------------------
@login_required(login_url="/login/")
def movie_list(request):

    movies = Movie.objects.all().order_by("-id")

    return render(request, "movies/movie_list.html", {
        "movies": movies
    })

    
@login_required(login_url="/login/")
def add_movie(request):

    if request.method == "POST":

        title = request.POST["title"]
        description = request.POST["description"]
        release_date = request.POST["release_date"]

        thumbnail = request.FILES.get("thumbnail")
        video = request.FILES.get("video_file")

        Movie.objects.create(
            title=title,
            description=description,
            release_date=release_date,
            thumbnail=thumbnail,
            video_file=video,
        )

        return redirect("movie_list")

    return render(request, "movies/add_movie.html")


# ----------------------------------
# Edit Movie (UPDATE)
# ----------------------------------
@login_required(login_url="/login/")
def edit_movie(request, id):

    movie = get_object_or_404(Movie, id=id)

    if request.method == "POST":

        movie.title = request.POST["title"]
        movie.description = request.POST["description"]
        movie.release_date = request.POST["release_date"]

        if request.FILES.get("thumbnail"):
            movie.thumbnail = request.FILES["thumbnail"]

        if request.FILES.get("video_file"):
            movie.video_file = request.FILES["video_file"]

        movie.save()

        return redirect("movie_list")

    return render(request, "movies/add_movie.html", {
        "movie": movie
    })

# ----------------------------------
# View Movie (DETAIL)
# ----------------------------------
@login_required(login_url="/login/")
def view_movie(request, id):

    movie = get_object_or_404(Movie, id=id)

    return render(request, "movies/view_details.html", {
        "movie": movie
    })


# ----------------------------------
# Delete Movie (DELETE)
# ----------------------------------
@login_required(login_url="/login/")
def delete_movie(request, id):

    movie = get_object_or_404(Movie, id=id)

    movie.delete()

    return redirect("movie_list")


# ----------------------------------
# Users
# ----------------------------------
@login_required(login_url="/login/")
def user_list(request):

    users = User.objects.filter(is_admin=False)

    return render(request, "users/users_list.html", {
        "users": users
    })
    
@login_required(login_url="/login/")
def block_user(request, id):

    user = get_object_or_404(User, id=id)
    user.is_active = False
    user.save()

    return redirect("user_list")


@login_required(login_url="/login/")
def unblock_user(request, id):

    user = get_object_or_404(User, id=id)
    user.is_active = True
    user.save()

    return redirect("user_list")

@login_required(login_url="/login/")
def delete_user(request, id):

    user = get_object_or_404(User, id=id)
    user.delete()

    return redirect("user_list")




@login_required(login_url="/login/")
def user_history(request, id):

    history = WatchHistory.objects.filter(user_id=id)

    return render(request, "users/view_history.html", {
        "history": history
    })

# ----------------------------------
# Reports
# ----------------------------------

@login_required(login_url="/login/")
def report(request):

    movies = Movie.objects.all().order_by("-view_count")

    total_views = Movie.objects.aggregate(
        total=Sum("view_count")
    )["total"] or 0

    return render(request, "report.html", {
        "movies": movies,
        "total_views": total_views
    })


# ----------------------------------
# Change Password
# ----------------------------------
@login_required(login_url="/login/")
def change_password(request):

    if request.method == "POST":

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        # Check current password
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect")
            return redirect("change_password")

        # Check new password match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match")
            return redirect("change_password")

        # Check minimum length
        if len(new_password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return redirect("change_password")

        # Set new password (hashed)
        user.set_password(new_password)
        user.save()

        # Keep user logged in
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully")

        return redirect("dashboard")

    return render(request, "auth/change_password.html")