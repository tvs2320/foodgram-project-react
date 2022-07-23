from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from .models import CustomUser, Follow


class CustomUserCreateSerializer(UserCreateSerializer):
    extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    # def set_password(self, validated_data):
    #     user = CustomUser(
    #         email=validated_data['email'],
    #         username=validated_data['username'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name'],
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    class Meta:
        model = CustomUser
        fields = ('email',
                  'username',
                  'first_name',
                  'last_name',
                  'password'
                  )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed'
                  )

    def get_is_subscribed(self, obj):
        follower = self.context['request'].user
        author = CustomUser.objects.get(id=obj.id)
        if Follow.objects.filter(follower=follower, author=author).exists():
            return True
        else:
            return False


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('follower', 'author',)
        model = Follow
