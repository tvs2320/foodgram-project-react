from django.core.validators import MinValueValidator
from django.db import models
from users.models import CustomUser


class Ingredients(models.Model):
    name = models.CharField(max_length=200, unique=True)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_and_measurement_unit'
            )
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)


class Tags(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)


class Recipes(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               db_index=True,
                               related_name='recipes',
                               verbose_name='Автор рецепта'
                               )
    ingredients = models.ManyToManyField(Ingredients,
                                         through='IngredientsAmount',
                                         related_name='recipes',
                                         verbose_name='Ингредиенты',
                                         )
    tags = models.ManyToManyField(Tags,
                                  related_name='recipes_tags',
                                  verbose_name='Теги')
    name = models.CharField(max_length=200, db_index=True, unique=True,
                            verbose_name='Название рецепта')
    image = models.ImageField(upload_to='recipes/', blank=True,
                              verbose_name='Загрузить фото')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1, 'Установите не меньше 1 минуты'), ],
        verbose_name='Время приготовления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)


class IngredientsAmount(models.Model):
    ingredients = models.ForeignKey(Ingredients,
                                    on_delete=models.CASCADE,
                                    related_name='amount',
                                    verbose_name='Ингредиенты',
                                    )
    recipes = models.ForeignKey(Recipes,
                                on_delete=models.CASCADE,
                                related_name='amount',
                                verbose_name='Рецепты', )
    amount = models.IntegerField()

    def __str__(self):
        return self.amount

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredients', 'recipes'],
                name='unique_ingredients_in_recipes'
            )
        ]
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'


class Favorite(models.Model):
    recipes = models.ForeignKey(Recipes,
                                on_delete=models.CASCADE,
                                related_name='favorites',
                                verbose_name='Рецепт'
                                )
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               verbose_name="Автор рецепта")

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipes', 'author'],
                name='unique_recipes_in_favorite'
            )
        ]
        verbose_name = 'Избранное'


class Basket(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='basket',
                               verbose_name='Автор рецепта'
                               )
    recipes = models.ForeignKey(Recipes,
                                on_delete=models.CASCADE,
                                related_name='basket',
                                verbose_name='Рецепты',
                                )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'recipes'],
                name='unique_recipe_in_basket'
            )
        ]
        verbose_name = 'Корзина'
