from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_VIEW_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerListViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)
        redirect_url = "/accounts/login/?next=/manufacturers/"

        self.assertRedirects(response, redirect_url)


class PrivateManufacturerListViewTests(TestCase):
    def setUp(self) -> None:
        # Create 8 test manufacturers for pagination tests
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user)
        number_of_manufacturers = 8
        for manufacturer_number in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Name {manufacturer_number}",
                country=f"Country {manufacturer_number}"
            )

    def test_list_view_url_exists_at_desired_location(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)

        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)
        template = "taxi/manufacturer_list.html"

        self.assertTemplateUsed(response, template)

    def test_pagination_is_five(self):
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)[:5]
        )
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["manufacturer_list"]) == 5)

    def test_lists_all_manufacturers(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(MANUFACTURER_LIST_VIEW_URL + "?page=2")
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)[-3:]
        )
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["manufacturer_list"]) == 3)
