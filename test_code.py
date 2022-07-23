
class RecipesCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientWriteSerializer(many=True, source='ingredientsamount')
    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(),
                                              many=True)

    def create_tags(self, tags, recipes):
        for tags in tags:
            recipes.tags.add(tags)

    # def create_ingredients(self, ingredients, recipes):
    #     for ingredients in ingredients:
    #         id = ingredients['id']
    #         amount = ingredients.get('amount')
    #         IngredientsAmount.objects.create(
    #             ingredients=id, amount=amount, recipes=recipes)

    def validate_author(self, value):
        return self.context['request'].user

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredientsamount')
        tags_data = validated_data.pop('tags')

        new_recipes = Recipes.objects.create(author=author, **validated_data)

        for ingredient in ingredients:
            id = ingredient["id"]
            amount = ingredient["amount"]
            IngredientsAmount.objects.create(
                ingredients=id, amount=amount, recipes=new_recipes)
        # self.create_ingredients(ingredients=ingredients_data,
        #                         recipes=new_recipes)
        self.create_tags(tags=tags_data,
                         recipes=new_recipes)

        return new_recipes

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)

        for data in ingredients_data:
            # ingredients = Ingredients.objects.get(id=data.get('id'))
            # ingredients.ingredients_name = data.get('ingredients_name', ingredients.ingredients_name)
            # ingredients.ingredients_measurement_unit = data.get('ingredients_measurement_unit', ingredients.ingredients_measurement_unit)
            ingredients = Ingredients.objects.get(**data)
            ingredients.save()
            instance.ingredients.add(ingredients)

        instance.tags.clear()
        tags = validated_data.get('tags')
        # for tag in tags:
        # recipes.tags.add(tag)
        # self.create_tags(tags, instance)

        # for tags in tags_data:
        #     # tags = Tags.objects.get(id=data)
        #     tags.save()
        #     # instance.tags.add(tags)

        # ingredients.save()
        instance.save()
        return instance

    class Meta:
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  )

        model = Recipes
        depth = 1


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientsAmountSerializer(
        source='ingredientsamount', many=True, read_only=True
    )
    tags = TagsSerializer(many=True)
    author = CustomUserSerializer()

    class Meta:
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  # 'is_favorited',
                  # 'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

        model = Recipes
        depth = 1

validated_data = {'ingredients': [OrderedDict([('ingredients', {'id': 1522}), ('amount', 100)]),
                                  OrderedDict([('ingredients', {'id': 5}), ('amount', 33)])],
                  'tags': [<Tags: Обед>, <Tags: Ужин>], 'name': 'цезарь',
'text': 'полезный и вкусный салат', 'cooking_time': 15, 'author': <CustomUser: admin>}


[OrderedDict([('ingredients', {'id': 1522}), ('amount', 100)]), OrderedDict([('ingredients', {'id': 5}), ('amount', 33)])]
