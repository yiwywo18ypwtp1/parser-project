from django.db import models
from django.db.models import CharField, EmailField, BooleanField


class Member(models.Model):
    full_name = CharField(max_length=100)
    license_number = CharField(max_length=20)
    license_type = CharField(max_length=20)
    license_status = CharField(max_length=20)

    email = EmailField(max_length=100)
    phone = CharField(max_length=20)
    fax = CharField(max_length=50, blank=True, null=True)
    website = CharField(max_length=50, blank=True, null=True)
    ttd = CharField(max_length=50, blank=True, null=True)

    private_practice = CharField(max_length=50)
    is_has_insurance = CharField(max_length=20)
    last_update = CharField(max_length=50)
    member_of_groups = CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.full_name} | {self.email}'


class Result(models.Model):
    name = CharField(max_length=50)
    link = CharField(max_length=255, null=True)
