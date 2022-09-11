from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from .models import CustomUser, Follow
from rest_framework.validators import UniqueTogetherValidator

from api.models import Recipes


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


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('follower', 'author',)
        model = Follow
        validators = [UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('follower', 'author'),
                message='Вы уже подписаны'
            )]


class FollowRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        follow = Follow.objects.filter(follower=request.user, author=obj)
        if follow.exists():
            return follow
        return 'У Вас еще нет подписок'

    def get_recipes(self, obj):
        request = self.context.get('request')
        context = {'request': request}
        if not request or request.user.is_anonymous:
            return False
        recipes = obj.recipes.all()
        return FollowRecipesSerializer(recipes, context=context, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
