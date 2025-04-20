from rest_framework.exceptions import ValidationError

domain_name = "youtube.com"


def url_validator(value):
    """Проверяет наличие ссылок на сторонние ресурсы. Разрешен только youtube.com"""
    if domain_name not in value:
        raise ValidationError("Ссылки на сторонние ресурcы кроме youtube.com запрещены")
