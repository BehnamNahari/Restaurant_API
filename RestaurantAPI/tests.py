from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from .models import Category, MenuItem, Rating, Order, Reservation


class RestaurantAPITestCase(APITestCase):
    def setUp(self):
        # ایجاد گروه‌ها
        self.manager_group = Group.objects.create(name='Manager')
        self.delivery_group = Group.objects.create(name='Delivery crew')
        self.owner_group = Group.objects.create(name='AppOwner')

        # ایجاد کاربران
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')
        self.manager = User.objects.create_user(username='manager', password='pass1234')
        self.manager.groups.add(self.manager_group)

        # ساخت دسته‌بندی و آیتم منو
        self.category = Category.objects.create(name="Pizza", slug="pizza")
        self.menu_item = MenuItem.objects.create(
            name="Margherita",
            price=10,
            description="Cheese pizza",
            category=self.category
        )

        # گرفتن توکن برای user1
        token_response = self.client.post(reverse('jwt-create'), {
            "username": "user1",
            "password": "pass1234"
        })
        self.assertEqual(token_response.status_code, 200)
        self.user1_token = token_response.data['access']

        # گرفتن توکن برای manager
        token_response_mgr = self.client.post(reverse('jwt-create'), {
            "username": "manager",
            "password": "pass1234"
        })
        self.assertEqual(token_response_mgr.status_code, 200)
        self.manager_token = token_response_mgr.data['access']

    def auth_as_user1(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')

    def auth_as_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.manager_token}')

    def test_menuitem_list_and_detail(self):
        url = reverse('menuitem-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data['results']), 1)

        detail_url = reverse('menuitem-detail', args=[self.menu_item.id])
        res = self.client.get(detail_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['name'], "Margherita")

    def test_create_rating_and_permissions(self):
        self.auth_as_user1()
        url = reverse('rating-list')
        res = self.client.post(url, {
            "menu_item": self.menu_item.id,
            "score": 8,
            "comment": "Good!"
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        rating_id = res.data['id']

        # کاربر دیگر نمی‌تواند این نظر را ویرایش کند
        token_response2 = self.client.post(reverse('jwt-create'), {
            "username": "user2",
            "password": "pass1234"
        })
        user2_token = token_response2.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {user2_token}')
        res_edit = self.client.patch(reverse('rating-detail', args=[rating_id]), {
            "comment": "Edited"
        })
        self.assertEqual(res_edit.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_and_visibility(self):
        self.auth_as_user1()
        url = reverse('order-list')
        res = self.client.post(url, {
            "delivery_address": "Street 123",
            "items": [
                {"menu_item_id": self.menu_item.id, "quantity": 2}
            ]
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order_id = res.data['id']

        # کاربر خودش می‌بیند
        res_my_orders = self.client.get(url)
        self.assertEqual(res_my_orders.status_code, 200)
        self.assertEqual(len(res_my_orders.data['results']), 1)
        # کاربر دیگر نمی‌بیند
        token_response2 = self.client.post(reverse('jwt-create'), {
            "username": "user2",
            "password": "pass1234"
        })
        user2_token = token_response2.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {user2_token}')
        res_other = self.client.get(url)
        self.assertEqual(len(res_other.data['results']), 0)

        # مدیر همه سفارش‌ها را می‌بیند
        self.auth_as_manager()
        res_mgr = self.client.get(url)
        self.assertGreaterEqual(len(res_mgr.data['results']), 1)

    def test_create_reservation_and_permissions(self):
        self.auth_as_user1()
        url = reverse('reservation-list')
        res = self.client.post(url, {
            "requested_at": "2030-01-01T12:00:00Z",
            "note": "Birthday",
            "guests_count": 4,
            "items": [
                {"menu_item_id": self.menu_item.id, "quantity": 1}
            ]
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        reservation_id = res.data['id']

        # کاربر دیگر نمی‌تواند حذف کند
        token_response2 = self.client.post(reverse('jwt-create'), {
            "username": "user2",
            "password": "pass1234"
        })
        user2_token = token_response2.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {user2_token}')
        res_del = self.client.delete(reverse('reservation-detail', args=[reservation_id]))
        self.assertEqual(res_del.status_code, status.HTTP_404_NOT_FOUND)

        # مدیر می‌تواند حذف کند
        self.auth_as_manager()
        res_del_mgr = self.client.delete(reverse('reservation-detail', args=[reservation_id]))
        self.assertIn(res_del_mgr.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])