from django.shortcuts import render
from django.http import Http404

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
