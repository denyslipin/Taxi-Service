from django.test import TestCase

from taxi.forms import DriverCreationForm, LicenseForm


class FormsTests(TestCase):
    def test_additional_fields_in_driver_creation_form(self):
        form_data = {
            "username": "test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "First Name",
            "last_name": "Last Name",
            "license_number": "Test license_number"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_update_form(self):
        correct_license_data = {"license_number": "ABC12345"}
        correct_form = LicenseForm(data=correct_license_data)

        wrong_license_data = {"license_number": "ABcd123a23"}
        wrong_form = LicenseForm(data=wrong_license_data)

        self.assertTrue(correct_form.is_valid())
        self.assertEqual(correct_form.cleaned_data, correct_license_data)

        self.assertFalse(wrong_form.is_valid())
        self.assertNotEqual(wrong_form.cleaned_data, wrong_license_data)
