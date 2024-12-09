from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import UserRegisterSerializer,MyTokenObtainPairSerializer
from . models import User
from rest_framework import status

# Create your views here.

class EmployeeRegistration(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        user = request.user 
        try:
            serializer = UserRegisterSerializer(user)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                username = serializer.validated_data['username'],
                email = serializer.validated_data['email'],
                password = serializer.validated_data['password'],
            )
            return Response({"message":"Registration Successfully completed"},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({"message":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not old_password or not new_password:
            return Response({"error": "Old password and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully!"}, status=status.HTTP_200_OK)