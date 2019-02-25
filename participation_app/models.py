from django.db import models


class Student(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_CHOICES = {
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    }
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def full_name(self):
        return self.first_name + ' ' + self.last_name
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_CHOICES,
        default=FRESHMAN,
    )

    def __str__(self):
        return self.first_name + ' ' + self.last_name
