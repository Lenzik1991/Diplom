from datetime import datetime
import pytest

from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from core.models import User
from goals.models import GoalCategory, BoardParticipant, Goal


@pytest.mark.django_db
def test_goal_detail(auth_client: APIClient, goal: Goal, test_user: User, board_participant: BoardParticipant) -> None:
    url = reverse('detail_update_delete_goal', kwargs={'pk': goal.id})
    response = auth_client.get(path=url)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response.status_code == status.HTTP_200_OK
    assert response_data['user']['id'] == test_user.pk
    assert response_data['user']['username'] == test_user.username
    assert response_data['user']['email'] == test_user.email


@pytest.mark.django_db
def test_goal_update(auth_client: APIClient, goal: Goal, test_user: User, goal_category: GoalCategory, board_participant: BoardParticipant) -> None:
    url = reverse('detail_update_delete_goal', kwargs={'pk': goal.id})
    test_date = str(datetime.now().date())
    payload = {
        'title': 'Новая цель',
        'category': goal_category.pk,
        'due_date': test_date,
        'description': 'Описание новой цели',
        'status': 1,
        'priority': 1
    }
    response = auth_client.patch(path=url, data=payload)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data['user']['id'] == test_user.pk
    assert response_data['user']['username'] == test_user.username
    assert response_data['user']['email'] == test_user.email


@pytest.mark.django_db
def test_goal_delete(auth_client: APIClient, goal: Goal, test_user: User, board_participant: BoardParticipant) -> None:
    url = reverse('detail_update_delete_goal', kwargs={'pk': goal.id})
    response = auth_client.delete(path=url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_goal_list(auth_client: APIClient, goal_list: Goal, board_participant: BoardParticipant) -> None:
    url = reverse('list_goal')
    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK
