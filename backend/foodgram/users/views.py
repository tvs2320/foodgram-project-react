from urllib import request
import pdb
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.response import Response  # Импортировали класс Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated, AllowAny)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from djoser.views import UserViewSet
from .models import CustomUser, Follow
from .permissions import IsAuthorOrReadOnly
from .serializers import CustomUserSerializer, FollowListSerializer, FollowSerializer
from api.pagination import FoodgramPagination


# class CustomUserViewSet(viewsets.ModelViewSet):
#     """Вьюсет данных пользователей.
#     Полный доступ к данным пользователей у администратора,
#     чтение/изменение данных своей учетной записи юзером"""
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = (AllowAny,)
#     pagination_class = PageNumberPagination
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter)
#     search_fields = ('username',)
#     ordering_fields = 'username'
#
#     @action(methods=['get', ], detail=False,
#             permission_classes=(IsAuthenticated,))
#     def me(self, request):
#         """Метод "me" отвечает за чтение пользователем
#         собственных учетных данных"""
#         me_user = self.request.user
#         serializer = self.get_serializer(me_user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#


class FollowViewSet(viewsets.ModelViewSet):
    """Набор представлений для модели Follow"""


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subscriptions(request):
    """Метод отвечающий за вывод страницы подписок"""
    context = {'request': request}
    author = request.user
    queryset = CustomUser.objects.filter(following__follower=author)
    page = FoodgramPagination.paginate_queryset(queryset, request)
    serializer = FollowListSerializer(page, context, many=True)
    return FoodgramPagination.get_paginated_response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def subscribe(request, id):
    """Метод отвечающий за подписку на автора"""
    follower = request.user
    author = get_object_or_404(CustomUser, id=id)

    if not Follow.objects.get(follower=follower, author=author).exists():
        data = {'follower': follower.id, 'author': id}
        serializer = FollowSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    follow = get_object_or_404(Follow, follower=follower, author=author)
    follow.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
# @api_view(['DELETE'], )
# @permission_classes([IsAuthenticated])
# def delete_subscribe(request, id):
#     """Метод отвечающий за удаление подписки на автора"""
#     follower = request.user
#     author = get_object_or_404(CustomUser, id=id)
#     follow = get_object_or_404(Follow, follower=follower, author=author)
#     follow.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)
