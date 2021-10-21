from django.db import models


class Abonent(models.Model):
    name = models.CharField(max_length=200)
    birthday = models.DateTimeField('birthday')
    address = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.name} was born {self.birthday} and live in {self.address}'


class Phone(models.Model):
    abonent = models.ForeignKey(Abonent, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.phone
