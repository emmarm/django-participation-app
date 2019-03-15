import math
import random
from django.views import generic
from django.views.generic.base import TemplateResponseMixin
from django.db.models import Min, Count

from .models import Student


class HomeView(generic.ListView):
    model = Student
    template_name = 'home.html'
    context_object_name = 'students'


class StudentView(generic.DetailView):
    model = Student
    template_name = 'student.html'
    context_object_name = 'student'


class ChosenView(TemplateResponseMixin, generic.View):
    template_name = 'chosen.html'

    def get_queryset(self):
        return Student.eligible_students.all()

    def get(self, request):
        eligible_students = self.get_queryset()
        point_awards = [
            (0, 'None'),
            (1, 'Minimal'),
            (2, 'Good'),
            (3, 'Great'),
            (5, 'Outstanding!')
        ]
        chosen = None
        if len(eligible_students) > 0:
            chosen_index = random.randrange(0, len(eligible_students))
            chosen = eligible_students[chosen_index]
        context = {
            'chosen': chosen,
            'point_awards': point_awards
        }
        self.render_to_response(context)


class AwardPointsView(TemplateResponseMixin, generic.View):
    template_name = 'points.html'

    def get_queryset(self):
        return Student.objects.filter()
