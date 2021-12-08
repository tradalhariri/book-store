from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Book
from django.urls import reverse

class BookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="trad", email="trad@gmail.com", password="pass"
        )

        self.book = Book.objects.create(
            title="Java", description="abc", publisher=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.book), "Java")

    def test_book_content(self):
        self.assertEqual(f"{self.book.title}", "Java")
        self.assertEqual(f"{self.book.publisher}", "trad@gmail.com")
        self.assertEqual(self.book.description, "abc")

    def test_book_list_view(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Java")
        self.assertTemplateUsed(response, "books/book_list.html")

    def test_book_detail_view(self):
        response = self.client.get(reverse("book_detail", args="1"))
        # no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "trad")
        self.assertTemplateUsed(response, "books/book_detail.html")

    def test_book_create_view(self):
        response = self.client.post(
            reverse("book_create"),
            {
                "title": "Python",
                "description": "django",
                "publisher": self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse("book_detail", args="2"))
        self.assertContains(response, "Python")

    def test_book_update_view_redirect(self):
        response = self.client.post(
            reverse("book_update", args="1"),
            {"title": "pascal","description":"xyz","publisher":self.user.id}
        )

        self.assertRedirects(response, reverse("book_detail", args="1"))

    def test_book_delete_view(self):
        response = self.client.get(reverse("book_delete", args="1"))
        self.assertEqual(response.status_code, 200)
