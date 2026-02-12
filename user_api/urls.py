from django.urls import path
from .views import Signup, add_to_watchlist, login, movie_detail, movie_list, get_watchlist, add_to_watchlist, get_watch_history, add_to_history, change_password

app_name = 'api'
urlpatterns = [
    path('signup/', Signup, name='signup'),
    path('login/', login, name='login'),
    path('movies/', movie_list, name='movie_list'),
    path('watchlist/add/', add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/', get_watchlist, name='get_watchlist'),
    path('history/add/', add_to_history, name='add_to_history'),
    path('history/', get_watch_history, name='get_watch_history'),
    path('change-password/', change_password, name='change_password'),
    path('movies/<int:pk>/', movie_detail),

]
