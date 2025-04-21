from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Ad, ExchangeProposal


class AdTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.client = APIClient()
        response = self.client.post(
            "/api/token/", {"username": "user", "password": "pass"}
        )
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_ad(self):
        # Проверяет создание объявления
        response = self.client.post(
            "/api/barter/",
            {
                "title": "Телефон",
                "description": "рабочий",
                "category": "Электроника",
                "condition": "used",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_ad(self):
        # Проверяет редактирование объявления
        ad = Ad.objects.create(
            user=self.user,
            title="Старый",
            description="desc",
            category="Техника",
            condition="used",
        )
        response = self.client.patch(f"/api/barter/{ad.id}/", {"title": "Новый"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Новый")

    def test_delete_ad(self):
        # Проверяет удаление объявления
        ad = Ad.objects.create(
            user=self.user,
            title="Удалить",
            description="desc",
            category="Техника",
            condition="used",
        )
        response = self.client.delete(f"/api/barter/{ad.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_barter(self):
        # Проверяет поиск объявлений по заголовку и описанию
        Ad.objects.create(
            user=self.user,
            title="Ноутбук",
            description="рабочий",
            category="Техника",
            condition="used",
        )
        response = self.client.get("/api/barter/?search=ноутбук")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data.get("results", [])), 1)


class ExchangeProposalTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass1")
        self.user2 = User.objects.create_user(username="user2", password="pass2")

        self.client = APIClient()
        token1 = self.client.post(
            "/api/token/", {"username": "user1", "password": "pass1"}
        ).data["access"]
        token2 = self.client.post(
            "/api/token/", {"username": "user2", "password": "pass2"}
        ).data["access"]

        self.token1 = token1
        self.token2 = token2

        self.ad1 = Ad.objects.create(
            user=self.user1,
            title="Ноут",
            description="desc",
            category="Техника",
            condition="used",
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title="Гитара",
            description="desc",
            category="Музыка",
            condition="new",
        )

    def test_create_proposal(self):
        # Проверяет создание предложения обмена
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token1}")
        response = self.client.post(
            "/api/proposals/",
            {"ad_sender": self.ad1.id, "ad_receiver": self.ad2.id, "comment": "Обмен?"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_accept_proposal_by_owner(self):
        # Проверяет принятие предложения владельцем ad_receiver
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token1}")
        response = self.client.post(
            "/api/proposals/",
            {"ad_sender": self.ad1.id, "ad_receiver": self.ad2.id, "comment": "Обмен?"},
        )
        proposal_id = response.data["id"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token2}")
        response = self.client.post(f"/api/proposals/{proposal_id}/accept/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "accepted")

    def test_reject_proposal_by_non_owner(self):
        # Проверяет запрет отклонения предложения не владельцем
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token1}")
        response = self.client.post(
            "/api/proposals/",
            {"ad_sender": self.ad1.id, "ad_receiver": self.ad2.id, "comment": "Обмен?"},
        )
        proposal_id = response.data["id"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token1}")
        response = self.client.post(f"/api/proposals/{proposal_id}/reject/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
