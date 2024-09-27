from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class GetPagesTestCase(TestCase):
    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'motorcycles/index.html')
        self.assertEqual(response.context_data['title'], "Главная страница")

    def test_redirect_addpage(self):
        path = reverse('addpublication')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)
