import math
import random
from django.shortcuts import render
from django.http import Http404
from django.db.models import Min, Count

from .models import Student


def home(req):
    students = Student.objects.all()
    return render(req, 'home.html', {'students': students})


def student(req, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        raise Http404('Student not found')
    return render(req, 'student.html', {'student': student})


def chosen(req):
    # get only present students and order by recently called
    students = Student.objects.exclude(present='AB').order_by('-last_called')
    # find number of times least called student was called
    least_called = students.aggregate(Min('times_called'))[
        'times_called__min']
    eligible_students = students.filter(
        times_called__lte=least_called * 1.4)[1:]
    chosen = random.randrange(0, len(eligible_students))
    return render(req, 'chosen.html', {'chosen': eligible_students[chosen]})
