from django.db import models

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Doctor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    specialization = models.CharField(choices={name: name for name in (
        'Cardiologist',
        'Dermatologist',
        'Orthopedic',
        'Pediatrist',
        'Physician',
        'Surgeon',
        'Neurologist',
        'Gynecologist',
        'Ostetrician',
        'Radiologist',
        'Dentist',
        'General pratictioner'
    )},
                                      max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)
    doctor = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    date = models.DateField(unique=True)
    time = models.TimeField()
    notes = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date}: {self.doctor} - {self.patient}"
