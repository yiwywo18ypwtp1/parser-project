from django.db import models
from django.db.models import CharField, EmailField, BooleanField


class Member(models.Model):
    full_name = CharField(max_length=100)
    license_number = CharField(max_length=100)
    license_type = CharField(max_length=100)
    license_status = CharField(max_length=100)

    email = EmailField(max_length=100, null=True)
    phone = CharField(max_length=100, null=True)
    fax = CharField(max_length=100, blank=True, null=True)
    website = CharField(max_length=100, blank=True, null=True)
    ttd = CharField(max_length=100, blank=True, null=True)

    private_practice = CharField(max_length=100, null=True)
    is_has_insurance = CharField(max_length=100, null=True)
    last_update = CharField(max_length=100, null=True)
    member_of_groups = CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.full_name} | {self.email}'


class Result(models.Model):
    status = CharField(max_length=20, null=True, default='New')
    link = CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.link} | {self.status}'
