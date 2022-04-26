from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django import forms

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "license_number",
        )


class LicenseForm(forms.ModelForm):
    LICENSE_NUMBER_LENGTH = 8
    LICENSE_NUMBER_UPPERCASE = 3
    LICENSE_NUMBER_DIGITS = 5

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        license_number = self.cleaned_data["license_number"]

        if len(license_number) != LicenseForm.LICENSE_NUMBER_LENGTH:
            raise ValidationError(
                "License Number must contain only "
                f"{LicenseForm.LICENSE_NUMBER_LENGTH} characters"
            )

        if not license_number[:LicenseForm.LICENSE_NUMBER_UPPERCASE].isupper():
            raise ValidationError(
                f"First {LicenseForm.LICENSE_NUMBER_UPPERCASE} "
                "characters must be uppercase"
            )

        if not license_number[-LicenseForm.LICENSE_NUMBER_DIGITS:].isdigit():
            raise ValidationError(
                f"Last {LicenseForm.LICENSE_NUMBER_DIGITS} "
                "characters must be digits"
            )

        return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Car
        fields = "__all__"


class CarSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by model..."})
    )
