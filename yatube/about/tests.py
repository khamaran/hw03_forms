from django.test import TestCase, Client
from http import HTTPStatus


class AboutURLTests(TestCase):
    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()

    def test_author_url_exists_at_desired_location(self):
        """Страница /author/ доступна любому пользователю."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech_added_url_exists_at_desired_location(self):
        """Страница /tech/ доступна любому пользователю."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
