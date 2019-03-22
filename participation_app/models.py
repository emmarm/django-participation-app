import math
import django
from django.db import models
from django.db.models import Sum, Min


class EligibleStudentsManager(models.Manager):
    def get_queryset(self):
        # get only present students and order by recently called
        students = super().get_queryset().exclude(
            present='AB').order_by('-last_called')
        if students:
            # find number of times least called student was called
            least_called = students.aggregate(Min('times_called'))[
                'times_called__min']
            # return only students called 1.4x least_called or less
            eligible_students = students.filter(
                times_called__lte=least_called * 1.4)
            # don't return most recently called students
            recently_called = math.floor(len(eligible_students) * 0.2)
            return eligible_students[recently_called:]
        else:
            return []


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
    full_name = models.CharField(max_length=100)
    last_called = models.DateTimeField(null=True, blank=True)
    participation_points = models.IntegerField(default=0)
    times_called = models.IntegerField(default=0)
    objects = models.Manager()
    eligible_students = EligibleStudentsManager()

    def get_full_name(self):
        return self.first_name.title() + ' ' + self.last_name.title()

    def get_last_called(self):
        return self.participations.order_by('-called').first().called

    def get_participation_points(self):
        points = Participation.objects.filter(
            student_id=self.pk).aggregate(Sum('points'))
        return points['points__sum']

    def get_times_called(self):
        return Participation.objects.filter(student_id=self.pk).count()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name()
        self.last_called = self.get_last_called()
        self.participation_points = self.get_participation_points()
        self.times_called = self.get_times_called()
        super(Student, self).save(*args, **kwargs)


class Participation(models.Model):
    points = models.IntegerField(default=0)
    called = models.DateTimeField(default=django.utils.timezone.now)
    student = models.ForeignKey(
        'Student', on_delete=models.CASCADE, related_name='participations')
