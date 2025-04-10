from django.db import models
from django.db.models import CharField, EmailField, BooleanField, TextField, IntegerField, JSONField, ImageField


class Member(models.Model):
    full_name = CharField(max_length=255)
    license_number = CharField(max_length=255)
    license_type = CharField(max_length=255)
    license_status = TextField()
    eligible_to_practice = CharField(max_length=50, blank=True, null=True)
    admit_date = CharField(max_length=100, blank=True, null=True)

    email = EmailField(max_length=100, null=True)
    phone = CharField(max_length=100, null=True)
    fax = CharField(max_length=100, blank=True, null=True)
    website = CharField(max_length=255, blank=True, null=True)
    ttd = CharField(max_length=255, blank=True, null=True)

    private_practice = TextField(blank=True, null=True)
    is_has_insurance = CharField(max_length=255, blank=True, null=True)
    last_update = CharField(max_length=100, blank=True, null=True)
    member_of_groups = TextField(blank=True, null=True)

    volunteer_service_history = JSONField(default=list, blank=True, null=True)

    firm_or_employer = TextField(blank=True, null=True)
    office_type_and_size = TextField(blank=True, null=True)
    practice_areas = TextField(blank=True, null=True)
    languages_other_than_english = TextField(blank=True, null=True)

    has_ever_was_as_judge = CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.full_name} | {self.email}'


class Result(models.Model):
    status = CharField(max_length=20, null=True, default='New')
    link = CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.link} | {self.status}'
