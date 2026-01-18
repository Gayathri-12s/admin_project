from django.shortcuts import render
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