from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from network.models import NetworkObject, Product
from network.serializers import NetworkObjectViewSerializer
from users.models import User


class NetworkAPITestCase(APITestCase):

    def setUp(self) -> None:
        """ Подготовка тестовой базы """

        super().setUp()
        self.user = User.objects.create(
            email='Test@mail.ru',
            is_staff=True,
            is_active=True
        )
        self.user.set_password('123456')
        self.user.save()
        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.product_1 = Product.objects.create(
            product_name='test_phone',
            model='125',
            release_date='2020-12-20'
        )
        self.product_2 = Product.objects.create(
            product_name='test_TV',
            model='845',
            release_date='2023-12-20'
        )

        self.network_factory = NetworkObject.objects.create(
            object_type='factory',
            name='Test factory',
            email='test@test.com',
            country='Россия',
            city='Москва',
            street='Тестовая',
            bld='5'
        )

        self.network_entrepreneur = NetworkObject.objects.create(
            object_type='entrepreneur',
            name='Test entrepreneur',
            email='entrepreneur@test.com',
            country='Россия',
            city='Тверь',
            street='Областная',
            bld='25',
            supplier=self.network_factory,
            debt=500
        )
        self.network_entrepreneur.products.add(self.product_1, self.product_2)

    def test_create(self):
        """ Тестирование создания объекта сети """

        data = {
            'object_type': 'retail',
            "name": 'Test retail',
            "email": 'retail@test.com',
            "country": 'Россия',
            "city": 'Москва',
            "street": 'Тестовая',
            "bld": '6',
            "supplier": self.network_factory.id,
            "debt": 1200,
            "products": [1, 2]
        }
        url = reverse('network:network-list')
        response = self.client.post(url, data=data)
        obj = NetworkObject.objects.get(email=data['email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(obj.hierarchy, 1)
        self.assertEqual(obj.name, data['name'])

    def test_list_view(self):
        """ Тестирование просмотра объектов"""

        url = reverse('network:network-list')
        response = self.client.get(url)
        serializer_data = NetworkObjectViewSerializer(
            [self.network_factory, self.network_entrepreneur],
            many=True
        ).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_detail_view(self):
        """ Тестирование просмотра 1 объекта"""

        url = reverse('network:network-detail', args=(self.network_entrepreneur.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], self.network_entrepreneur.name)

    def test_update(self):
        """ Тестирование изменения объекта"""

        url = reverse('network:network-detail', args=(self.network_entrepreneur.pk,))
        response = self.client.patch(url, {'name': 'new name'})
        self.network_entrepreneur.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.network_entrepreneur.name, 'new name')







