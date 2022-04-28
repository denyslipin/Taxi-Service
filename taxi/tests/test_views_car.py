from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

CAR_LIST_VIEW_URL = reverse("taxi:car-list")


class PublicCarListViewTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_VIEW_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(CAR_LIST_VIEW_URL)
        redirect_url = "/accounts/login/?next=/cars/"

        self.assertRedirects(response, redirect_url)


class PrivateCarListViewTests(TestCase):
    def setUp(self) -> None:
        # Create 8 test cars for pagination tests
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345"
        )
        self.client.force_login(self.user)
        number_of_cars = 8
        manufacturer1 = Manufacturer.objects.create(
            name="BMW Group",
            country="Germany"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Honda Motor",
            country="Japan"
        )
        for car_number in range(number_of_cars):
            if car_number % 2 == 0:
                Car.objects.create(
                    model=f"Model {car_number}",
                    manufacturer=manufacturer1
                )
            else:
                Car.objects.create(
                    model=f"Name {car_number}",
                    manufacturer=manufacturer2
                )

    def test_list_view_url_exists_at_desired_location(self):
        response = self.client.get(CAR_LIST_VIEW_URL)

        self.assertEqual(response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        response = self.client.get(CAR_LIST_VIEW_URL)
        template = "taxi/car_list.html"

        self.assertTemplateUsed(response, template)

    def test_pagination_is_five(self):
        response = self.client.get(CAR_LIST_VIEW_URL)
        cars = Car.objects.all()

        self.assertEqual(list(response.context["car_list"]), list(cars)[:5])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["car_list"]) == 5)

    def test_lists_all_cars(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(CAR_LIST_VIEW_URL + "?page=2")
        cars = Car.objects.all()

        self.assertEqual(list(response.context["car_list"]), list(cars)[-3:])
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["car_list"]) == 3)

    def test_search_form(self):
        response1 = self.client.get(CAR_LIST_VIEW_URL + "?model=MO")
        cars1 = Car.objects.filter(model__istartswith="mo")

        response2 = self.client.get(CAR_LIST_VIEW_URL + "?model=na")
        cars2 = Car.objects.filter(model__istartswith="NA")

        self.assertEqual(list(response1.context["car_list"]), list(cars1))
        self.assertEqual(list(response2.context["car_list"]), list(cars2))
