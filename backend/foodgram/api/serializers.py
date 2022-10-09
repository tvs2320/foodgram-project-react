from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Basket, Favorite, Ingredients, IngredientsAmount,
                            Recipes, Tags)
from users.serializers import CustomUserSerializer


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class IngredientWriteSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'amount')


class IngredientsAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

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
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipes
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'image',
                  'name',
                  'text',
                  'cooking_time')

    def get_ingredients(self, obj):
        ingredients = IngredientsAmount.objects.filter(recipes=obj)
        return IngredientsAmountSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False
        author = request.user
        return Favorite.objects.filter(author=author, recipes=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated:
            return False
        author = request.user
        return Basket.objects.filter(author=author, recipes=obj).exists()


class RecipesCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientWriteSerializer(many=True)
    image = Base64ImageField()

    def validate(self, data):
        # Проверка, что время готовки больше нуля
        if data['cooking_time'] < 1:
            return 'Меньше чем за минуту ничего не приготовить!!!'
        # Проверка, что пришли ингредиенты
        elif len(data['ingredients']) < 1:
            return 'Укажите хотя бы один ингредиент в рецепте'
        # Проверка, что пришли теги
        elif len(data['tags']) is None:
            return 'Укажите хотя бы один тег в рецепте'
        # Проверка, что ингредиенты не повторяются
        ingredients = self.initial_data.get('ingredients')
        ingr_list = []
        for ingr in ingredients:
            if ingr['id'] in ingr_list:
                return 'Нельзя указывать 2 одинаковых ингредиента'
            ingr_list.append(ingr['id'])
        # Проверка, что количество ингредиента больше нуля
            if int(ingr['amount']) <= 0:
                return f'Укажите кол-во для ингредиента больше 0'

        return data

    def create_ingredients(self, recipes, ingredients):
        IngredientsAmount.objects.bulk_create([
            IngredientsAmount(
                recipes=recipes,
                ingredients=i['id'],
                amount=i['amount'],
            ) for i in ingredients
        ])

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        new_recipes = Recipes.objects.create(**validated_data)
        self.create_ingredients(new_recipes, ingredients_data)
        new_recipes.tags.set(tags)
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
        instance.tags.set(tags_data)

        instance.ingredients.clear()
        ingredients_data = validated_data.pop('ingredients')
        self.create_ingredients(instance, ingredients_data)

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


class CutRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('author', 'recipes')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipes = data['recipes']
        if Favorite.objects.filter(
                author=request.user, recipes=recipes).exists():
            return 'Рецепт уже есть в избранном!'
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return CutRecipesSerializer(
            instance.recipes, context=context).data


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('author', 'recipes')

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipes = data['recipes']
        if Basket.objects.filter(author=request.user,
                                 recipes=recipes
                                 ).exists():
            return 'Рецепт уже есть в списке покупок!'
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return CutRecipesSerializer(
            instance.recipes, context=context).data
