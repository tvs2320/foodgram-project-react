from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, Follow
from .serializers import FollowListSerializer, FollowSerializer
from api.pagination import FoodgramPagination


class FollowListAPIView(ListAPIView):
    """Вывод подписок пользователя"""
    pagination_class = FoodgramPagination
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = CustomUser.objects.filter(following__follower=request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class FollowApiView(APIView):
    """Создание и удаление подписок"""
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        """Метод, отвечающий за создание подписок"""
        data = {'follower': request.user.id, 'author': id}
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        """Метод, отвечающий за удаление подписок"""
        follower = request.user
        author = get_object_or_404(CustomUser, id=id)
        follow = get_object_or_404(
            Follow, follower=follower, author=author
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
