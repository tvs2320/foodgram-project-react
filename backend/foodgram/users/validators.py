from django.core.exceptions import ValidationError


def username_validate(value):
    if value == 'me':
        raise ValidationError('Пожалуйста, придумайте другое имя')
    return value
