from django.contrib.sites import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient
from todolist.settings import TG_BOT_API_TOKEN


class BotVerifyView(UpdateAPIView):
    queryset = TgUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TgUserSerializer

    def patch(self, request: requests, *args: str, **kwargs: int) -> Response:
        ver_code = request.data.get('verification_code')

        if not ver_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            tg_user: TgUser = self.get_queryset().get(verification_code=ver_code)
        except TgUser.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        tg_user.user = self.request.user
        tg_user.verification_code = None
        tg_user.save()
        TgClient(token=TG_BOT_API_TOKEN).send_message(tg_user.tg_chat_id, 'Успешно')
        return Response(status=status.HTTP_200_OK)

