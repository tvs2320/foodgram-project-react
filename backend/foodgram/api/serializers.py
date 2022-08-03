from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from .models import Ingredients, Tags, Recipes, IngredientsAmount
from django.core.validators import MinValueValidator
from users.models import CustomUser
import pdb

from users.serializers import CustomUserSerializer


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class IngredientWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class IngredientsAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  # 'is_favorite',
                  # 'is_in_shopping_cart',
                  'image',
                  'name',
                  'text',
                  'cooking_time')

    def get_ingredients(self, obj):
        ingredients = IngredientsAmount.objects.filter(recipes=obj)
        return IngredientsAmountSerializer(ingredients, many=True).data


class RecipesCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientWriteSerializer(many=True)

    def create_tags(self, tags, recipes):
        for tags in tags:
            recipes.tags.add(tags)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        new_recipes = Recipes.objects.create(**validated_data)

        for data in ingredients_data:
            ingr = get_object_or_404(Ingredients, pk=data['id'])
            amount = data['amount']
            IngredientsAmount.objects.create(recipes=new_recipes,
                                             ingredients=ingr,
                                             amount=amount)
        self.create_tags(recipes=new_recipes,
                         tags=tags)

        return new_recipes

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)

        instance.tags.clear()
        tags_data = validated_data.get('tags')
        self.create_tags(tags=tags_data, recipes=instance)

        instance.ingredients.clear()
        ingredients_data = validated_data.pop('ingredients')
        for data in ingredients_data:
            ingr = get_object_or_404(Ingredients, pk=data['id'])
            amount = data['amount']
            IngredientsAmount.objects.create(recipes=instance,
                                             ingredients=ingr,
                                             amount=amount)

        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipesSerializer(instance, context=self.context).data

    class Meta:
        model = Recipes
        fields = ('author',
                  'ingredients',
                  'tags',
                  'image',
                  'name',
                  'text',
                  'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    pass
