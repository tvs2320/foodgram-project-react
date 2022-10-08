from django.db.models import Sum
from django.http import HttpResponse
from recipes.models import (IngredientsAmount)


def report(request):
    """Метод отвечающий за выгрузку файла со списком ингридиентов
    из рецептов, сохраненных в список покупок"""
    basket = IngredientsAmount.objects.filter(
        recipes__basket__author=request.user)
    ingredients_list = basket.values('ingredients__name',
                                     'ingredients__measurement_unit'
                                     ).annotate(total=Sum('amount'))
    file = ''
    shopping_cart = list()
    for ingredient in ingredients_list:
        if ingredient["ingredients__name"] not in shopping_cart:
            value = (f'{ingredient["ingredients__name"]} - '
                     f'{ingredient["total"]} '
                     f'{ingredient["ingredients__measurement_unit"]}')
            shopping_cart.append(ingredient["ingredients__name"])
            file += value + '\n'
    filename = 'shopping_cart.txt'
    response = HttpResponse(file, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
