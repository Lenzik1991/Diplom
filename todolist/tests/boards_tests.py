import json

import pytest
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient
from core.models import User
from goals.serializers import BoardSerializer
from goals.models import BoardParticipant, Board


@pytest.mark.django_db
def test_board_create(auth_client: APIClient) -> None:
    url = reverse('create_board')
    payload = {
        'title': 'Название доски',
        'is_deleted': False
    }
    response = auth_client.post(url, data=payload)
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['title'] == payload['title']
    assert response_data['is_deleted'] == payload['is_deleted']


@pytest.mark.django_db
def test_board_detail(auth_client: APIClient, test_user: User, board: Board, board_participant: BoardParticipant) -> None:
    url = reverse('detail_update_delete_board', kwargs={'pk': board.id})
    response = auth_client.get(url)
    response_data = response.json()
    expected_data = BoardSerializer(board).data

    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_data


@pytest.mark.django_db
def test_board_update(auth_client: APIClient, test_user: User, board: Board, board_participant: BoardParticipant) -> None:
    url = reverse('detail_update_delete_board', kwargs={'pk': board.id})
    payload = {
        'participants': [],
        'title': 'Переименование доски'
    }
    response = auth_client.put(url, data=json.dumps(payload), content_type='application/json')
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data['id'] == board.id
    assert response_data['participants'][0]['id'] == board_participant.pk
    assert response_data['participants'][0]['user'] == test_user.username


@pytest.mark.django_db
def test_board_delete(auth_client: APIClient, test_user: User, board: Board, board_participant: BoardParticipant) -> None:
    url = reverse('detail_update_delete_board', kwargs={'pk': board.id})
    response = auth_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_board_list(auth_client: APIClient, test_user: User, board_list: Board) -> None:
    board_participant = []
    for board_ in board_list:
        board_participant.append(BoardParticipant.objects.create(board=board_, user=test_user))
    url = reverse('list_board')
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_200_OK

