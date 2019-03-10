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
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_CHOICES,
        default=FRESHMAN,
    )
    ON_TIME = 'OT'
    TARDY = 'TR'
    ABSENT = 'AB'
    PRESENT_CHOICES = {
        (ON_TIME, 'On-Time'),
        (TARDY, 'Tardy'),
        (ABSENT, 'Absent')
    }
    present = models.CharField(
        max_length=2,
        choices=PRESENT_CHOICES,
        default=ABSENT
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    participation_points = models.IntegerField(default=0)
    times_called = models.IntegerField(default=0)
    last_called = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
