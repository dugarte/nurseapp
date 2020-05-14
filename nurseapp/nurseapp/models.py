from django.db import models
from django.utils import timezone


class Patient(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    identity_card_number = models.TextField(null=False, unique=True)
    name = models.TextField(null=False)
    age = models.IntegerField(null=False)
    date_added = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        db_table = 'patient'
        managed = True


class VitalSign(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    date_added = models.DateTimeField(default=timezone.now, null=False)
    heart_rate = models.IntegerField(null=False)
    systolic = models.IntegerField(null=False)
    diastolic = models.IntegerField(null=False)
    age = models.IntegerField(null=False)
    heart_rate_status = models.TextField(null=False)
    blood_pressure_status = models.TextField(null=False)

    class Meta:
        db_table = 'vital_sign'
        managed = True
