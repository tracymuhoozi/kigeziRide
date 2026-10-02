from django.core.validators import RegexValidator
#  Ugandan numbers in international format, e.g. +256772123456
uganda_phone_validator = RegexValidator(
    regex=r"^\+256\d{9}$",
    message="Enter a Ugandan phone number in the format +256XXXXXXXXX.",
)


