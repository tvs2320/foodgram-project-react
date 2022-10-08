
from django.core.exceptions import ValidationError
from recipes.models import Recipes
from django.forms.models import BaseInlineFormSet


class RecipesForm(BaseInlineFormSet):
    class Meta:
        model = Recipes
        fields = ('author', 'ingredients', 'tags', 'name', 'image', 'text',
                  'cooking_time')

    def clean_ingredients(self):
        ingredients = self.cleaned_data['ingredients']
        if ingredients is None:
            raise ValidationError('Укажите не менее одного ингредиента')
        return ingredients
