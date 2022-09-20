from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from .models import CustomUser, Follow
from rest_framework.validators import UniqueTogetherValidator
import pdb
from api.models import Recipes
import json


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериалайзер создания пользователя"""
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
    """Сериалайзер вывода данных о пользователе"""
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
        """Метод, указывающий на наличие/отсутствие подписки на
         пользователя из запроса"""
        follower = self.context['request'].user
        author = CustomUser.objects.get(id=obj.id)
        if Follow.objects.filter(follower=follower, author=author).exists():
            return True
        else:
            return False


class FollowSerializer(serializers.ModelSerializer):
    """Сериалайзер создания подписок"""
    class Meta:
        fields = ('follower', 'author',)
        model = Follow
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=('follower', 'author'),
            message='Вы уже подписаны'
        )]

    def validate(self, attrs):
        """Метод, отвечающий за проверку корректности создаваемой подписки"""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return attrs

    def to_representation(self, instance):
        """Метод, отвечающий за получение списка подписок"""
        request = self.context.get('request')
        context = {'request': request}
        return FollowListSerializer(instance.author,
                                    context=context).data


class FollowRecipesSerializer(serializers.ModelSerializer):
    """Сериалайзер вывода данных о рецептах в подписках"""
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(serializers.ModelSerializer):
    """Сериалайзер вывода подписок"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """Метод получения подписок пользователя"""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(follower=request.user, author=obj).exists()

    def get_recipes(self, obj):
        """Метод получения рецептов из подписок пользователя"""
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        context = {'request': request}
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit is not None:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        else:
            recipes = obj.recipes.all()
        return FollowRecipesSerializer(
            recipes, many=True, context=context).data

    def get_recipes_count(self, obj):
        """Метод получения количества рецептов в подписках"""
        return Recipes.objects.filter(author=obj).count()
