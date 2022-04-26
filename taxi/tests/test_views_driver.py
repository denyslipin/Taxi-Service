from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_VIEW_URL = reverse("taxi:driver-list")
DRIVER_CREATE_VIEW_URL = reverse("taxi:driver-create")


class PublicDriverListViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(DRIVER_LIST_VIEW_URL)
        redirect_url = "/accounts/login/?next=/drivers/"

        self.assertRedirects(response, redirect_url)


class PublicDriverCreateViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_CREATE_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(DRIVER_CREATE_VIEW_URL)
        redirect_url = "/accounts/login/?next=/drivers/create/"

        self.assertRedirects(response, redirect_url)


class PrivateDriverListViewTests(TestCase):
    def setUp(self) -> None:
        # Create 8 drivers (1 user and 7 test drivers) for pagination tests
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user)
        number_of_drivers = 7
        for driver_number in range(number_of_drivers):
            Driver.objects.create(
                username=f"Name {driver_number}",
                first_name=f"First Name {driver_number}",
                last_name=f"Last Name {driver_number}",
                license_number=f"License number {driver_number}"
            )

    def test_list_view_url_exists_at_desired_location(self):
        response = self.client.get(DRIVER_LIST_VIEW_URL)

        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        response = self.client.get(DRIVER_LIST_VIEW_URL)
        template = "taxi/driver_list.html"

        self.assertTemplateUsed(response, template)

    def test_pagination_is_five(self):
        response = self.client.get(DRIVER_LIST_VIEW_URL)
        drivers = Driver.objects.all()

        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)[:5]
        )
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["driver_list"]) == 5)

    def test_lists_all_drivers(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(DRIVER_LIST_VIEW_URL + '?page=2')
        drivers = Driver.objects.all()

        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)[-3:]
        )
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["driver_list"]) == 3)


class PrivateDriverCreateViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user)

    def test_create_view_url_exists_at_desired_location(self):
        response = self.client.get(DRIVER_CREATE_VIEW_URL)

        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        response = self.client.get(DRIVER_CREATE_VIEW_URL)
        template = "taxi/driver_form.html"

        self.assertTemplateUsed(response, template)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "First Name",
            "last_name": "Last Name",
            "license_number": "Test license_number"
        }
        self.client.post(DRIVER_CREATE_VIEW_URL, data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
