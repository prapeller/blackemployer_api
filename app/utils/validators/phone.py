from django.core.exceptions import ValidationError


def validate_phone(value):
    if not (value[0] == "+" and value[1] == "7" and len(value) == 12):
        raise ValidationError(
            "Неверный формат телефона",
        )


def validate_few_phones(value):
    phones = value.split(",")
    for phone in phones:
        validate_phone(phone)
