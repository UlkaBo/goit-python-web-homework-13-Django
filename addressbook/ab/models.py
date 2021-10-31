from django.db import models
from django.conf import settings


class Abonent(models.Model):
    name = models.CharField(max_length=200)
    birthday = models.DateTimeField('birthday')
    address = models.CharField(max_length=300)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="owner of abonent",
        on_delete=models.CASCADE,
        related_name="abonents")

    def __str__(self):
        return f'{self.name} was born {self.birthday} and live in {self.address}'


class Phone(models.Model):
    abonent = models.ForeignKey(Abonent, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.phone
