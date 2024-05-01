from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    
    SMOKER_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    # Adjusting choices to numerical values as per your original code
    CHOLESTEROL_CHOICES = [
        (159, 'Less than 160'),
        (160, '160 - 199'),
        (200, '200 - 239'),
        (240, '240 - 279'),
        (280, '280 and above'),
    ]

    HDL_CHOICES = [
        (39, 'Less than 40'),
        (40, '40 - 49'),
        (50, '50 - 59'),
        (60, '60 and above'),
    ]

    BLOOD_PRESSURE_CHOICES = [
        (119, 'Less than 120'),
        (120, '120 - 129'),
        (130, '130 - 139'),
        (140, '140 - 159'),
        (160, '160 - 179'),
        (180, '180 and above'),
    ]

    gender = models.CharField(
        max_length=6,  # Adjusted for the length of 'FEMALE'
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )

    age = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    total_cholesterol = models.PositiveIntegerField(
        choices=CHOLESTEROL_CHOICES,
        blank=True,
        null=True
    )

    hdl_cholesterol = models.PositiveIntegerField(
        choices=HDL_CHOICES,
        blank=True,
        null=True
    )

    blood_pressure = models.PositiveIntegerField(
        choices=BLOOD_PRESSURE_CHOICES,
        blank=True,
        null=True
    )

    is_smoker = models.CharField(
        max_length=3,  # Adjusted to fit 'YES' and 'NO'
        choices=SMOKER_CHOICES,
        blank=True,
        null=True
    )

    risk = models.FloatField(
        blank=True,
        null=True
    )

    # Auto add current date only
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Patient {self.id}'