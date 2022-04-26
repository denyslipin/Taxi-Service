from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        result_str = f"{manufacturer.name} ({manufacturer.country})"

        self.assertEqual(str(manufacturer), result_str)


class DriverModelTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="First Name",
            last_name="Last Name",
            license_number="Test license_number"
        )

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test12345"
        license_number = "Test license_number"

        self.assertEqual(self.driver.username, username)
        self.assertTrue(self.driver.check_password(password))
        self.assertEqual(self.driver.license_number, license_number)

    def test_driver_get_absolute_url(self):
        result_url = reverse("taxi:driver-detail", args=[self.driver.id])

        self.assertEquals(self.driver.get_absolute_url(), result_url)

    def test_driver_str(self):
        result_str = f"{self.driver.username} " \
                     f"({self.driver.first_name} {self.driver.last_name})"

        self.assertEqual(str(self.driver), result_str)


class CarModelTest(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        result_str = f"{car.model} ({manufacturer.name})"

        self.assertEqual(str(car), result_str)
