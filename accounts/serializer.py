from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model = User
        fields = ['username','email','password','confirm_password']

    def validate(self,data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        username = data.get('username')

        length = len(password)

        if length<4:
            raise serializers.ValidationError({'error':'Password must need 8 charecters'})
            
        if password != confirm_password:
            raise serializers.ValidationError({'error':'password doesnt match'})
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'error': 'Username is already taken'})
        
        return data
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)  
        token['username'] = user.username
        token['email'] = user.email  
        return token