# accounts/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

# 회원가입 전용 (비밀번호 write_only)
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'password', 'password2', 'name',
            'birth_date', 'gender', 'phone_number',
            'address', 'is_guardian', 'guardian_for'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2": "2차 비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(
            user_id=validated_data['user_id'],
            name=validated_data['name'],
            password=validated_data['password'],
            birth_date=validated_data['birth_date'],
            address=validated_data['address'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],
            is_guardian=validated_data.get('is_guardian', False),
            guardian_for=validated_data.get('guardian_for', '')
        )
        return user

# 조회, 수정용
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id', 'name', 'birth_date', 'gender',
            'phone_number', 'address', 'is_guardian', 'guardian_for'
        ]
        read_only_fields = ['user_id', 'gender', 'is_guardian', 'guardian_for']


# UserDetail을 작성하는 부분
from .models import UserDetail

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = '__all__'
        read_only_fields = ['user']
