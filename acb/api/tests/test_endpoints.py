import pytest
import random
import re

from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers import MatchEventSerializer

base_game_id = 103789
num_games = 10
random_game_ids = [base_game_id + random.randint(-1000, 1000) for _ in range(num_games)]


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def authenticated_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


def isinstance_or_none(value, expected_type):
    return isinstance(value, (expected_type, type(None)))


@pytest.mark.django_db
def test_pbp_lean_ok(authenticated_client):
    for game_id in random_game_ids:
        url = reverse('acb-api:pbp-lean', args=[game_id])
        response = authenticated_client.get(url)
        serializer = MatchEventSerializer(data=response.data, many=True)

        assert response.status_code == status.HTTP_200_OK
        assert serializer.is_valid(), serializer.errors
        assert response.json() == serializer.data

        for el in serializer.data:
            assert isinstance_or_none(el["team_id"], int)
            assert isinstance_or_none(el["player_license_id"], int)
            assert isinstance_or_none(el["action_time"], str)
            assert isinstance(el["action_type"], int)
            assert el["team_id"] >= 0 if el["team_id"] else True
            assert el["player_license_id"] >= 0 if el["player_license_id"] else True
            assert re.match(r'^\d{2}:\d{2}:\d{2}$', el["action_time"]) is not None if el["action_time"] else True
            assert el["action_type"] >= 0


@pytest.mark.django_db
def test_game_leaders_ok(authenticated_client):
    for game_id in random_game_ids:
        url = reverse('acb-api:game-leaders', args=[game_id])
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), dict)
        assert len(response.json().keys()) == 2
        assert "home_team_leaders" in response.json()
        assert "away_team_leaders" in response.json()

        for v in response.json().values():
            for el in v:
                assert isinstance(el[0], int)
                assert isinstance(el[1]["name"], str)
                assert isinstance(el[1]["points"], int)
                assert isinstance(el[1]["rebounds"], int)
                assert el[0] >= 0
                assert el[1]["points"] >= 0
                assert el[1]["rebounds"] >= 0


@pytest.mark.django_db
def test_game_biggest_lead_ok(authenticated_client):
    for game_id in random_game_ids:
        url = reverse('acb-api:game-biggest-lead', args=[game_id])
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), dict)
        assert len(response.json().keys()) == 2
        assert "home_team" in response.json()
        assert "away_team" in response.json()

        for k in response.json().keys():
            assert isinstance(response.json()[k], int)
            assert response.json()[k] >= 0


@pytest.mark.django_db
def test_all_endpoint_urls_no_auth(api_client):
    urls = [
        reverse('acb-api:pbp-lean', args=[random.choice(random_game_ids)]),
        reverse('acb-api:game-leaders', args=[random.choice(random_game_ids)]),
        reverse('acb-api:game-biggest-lead', args=[random.choice(random_game_ids)]),
    ]

    for url in urls:
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Authentication credentials were not provided."}