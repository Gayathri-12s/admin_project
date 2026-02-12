from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,  HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from django.http import JsonResponse
from admin_app.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from admin_app.models import Movie    
from .serializers import MovieSerializer
from rest_framework.permissions import IsAuthenticated
from admin_app.models import Watchlist
from .serializers import WatchlistSerializer
from admin_app.models import WatchHistory
from .serializers import WatchHistorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status



@api_view(['POST'])
@permission_classes((AllowAny,))


def Signup(request):
        email  = request.data.get("email")
        password = request.data.get("password")

        
       
        name = request.data.get("name")
        if not name or not email or not password:
            return Response({'message':'All fields are required'})
        if User.objects.filter(email=email).exists():
            return  JsonResponse({'message':'Email already exist'})
        user = User.objects.create_user(email=email,password=password)
        user.name = name
        user.save()
        return JsonResponse({'message':'user created successsfully'} ,status = 200)
    
    

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)




@api_view(['GET'])
@permission_classes([AllowAny])
def movie_list(request):
    movies = Movie.objects.all().order_by('-view_count')
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def movie_detail(request, pk):

    movie = get_object_or_404(Movie, pk=pk)

    # GET = View Details
    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    # PUT = Update (Admin)
    if request.method == 'PUT':
        serializer = MovieSerializer(
            movie,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_watchlist(request):
    movie_id = request.data.get("movie_id")

    Watchlist.objects.get_or_create(
        user=request.user,
        movie_id=movie_id
    )

    return Response({"message": "Added to watchlist"})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    serializer = WatchlistSerializer(watchlist, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_history(request):
    movie_id = request.data.get("movie_id")

    if not movie_id:
        return Response(
            {"error": "movie_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response(
            {"error": "Movie not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    WatchHistory.objects.create(
        user=request.user,
        movie=movie
    )

  
    movie.view_count += 1
    movie.save()

    return Response(
        {"message": "Watch history updated"},
        status=status.HTTP_201_CREATED
    )



@api_view(['GET'])
@permission_classes([IsAuthenticated])      
def get_watch_history(request):
    history = WatchHistory.objects.filter(user=request.user).order_by('-watched_at')
    serializer = WatchHistorySerializer(history, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user

    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")
    confirm_password = request.data.get("confirm_password")

 
    if not old_password or not new_password or not confirm_password:
        return Response(
            {"error": "All fields are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not user.check_password(old_password):
        return Response(
            {"error": "Old password is incorrect"},
            status=status.HTTP_400_BAD_REQUEST
        )

   
    if new_password != confirm_password:
        return Response(
            {"error": "New password and confirm password do not match"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(new_password)
    user.save()

    return Response(
        {"message": "Password changed successfully"},
        status=status.HTTP_200_OK
    )
