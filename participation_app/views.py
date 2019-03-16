import math
import random
from django.views import generic
from django.shortcuts import redirect
from django.views.generic.base import TemplateResponseMixin
from django.db.models import Min, Count

from .models import Student, Participation


class HomeView(generic.ListView):
    model = Student
    template_name = 'home.html'
    context_object_name = 'students'


class StudentView(generic.DetailView):
    model = Student
    template_name = 'student.html'
    context_object_name = 'student'


class ChooseView(generic.View):
    def get_queryset(self):
        eligible_students = Student.eligible_students.all()
        chosen = None
        if len(eligible_students) > 0:
            chosen_index = random.randrange(0, len(eligible_students))
            chosen = eligible_students[chosen_index]
        return chosen

    def get(self, request):
        chosen_student = self.get_queryset()
        return redirect('chosen', pk=chosen_student.id)


class ChosenView(generic.DetailView):
    model = Student
    template_name = 'chosen.html'
    point_awards = [
        (0, 'None'),
        (1, 'Minimal'),
        (2, 'Good'),
        (3, 'Great'),
        (5, 'Outstanding!')
    ]
    context_object_name = 'chosen'
    extra_context = {
        'point_awards': point_awards
    }

    # def get_queryset(self, pk):
    #     return Student.objects.filter(id=pk).first()

    # def get(self, request, pk):
    #     chosen = self.get_queryset(pk)
    #     point_awards = [
    #         (0, 'None'),
    #         (1, 'Minimal'),
    #         (2, 'Good'),
    #         (3, 'Great'),
    #         (5, 'Outstanding!')
    #     ]
    #     context = {
    #         'chosen': chosen,
    #         'point_awards': point_awards
    #     }
    #     return self.render_to_response(context)


class AwardPointsView(generic.View):
    def get_queryset(self, pk):
        return Student.objects.get(pk=pk)

    def post(self, request, pk):
        points = request.POST.get('points', None)
        try:
            student = self.get_queryset(pk)
        except (KeyError, Student.DoesNotExist):
            return redirect('home')
        else:
            participation = Participation(
                points=points,
                student=student
            )
            participation.save(force_insert=True)
            student.save()
            return redirect('award_points', pk=pk)


class PointsAwardedView(TemplateResponseMixin, generic.View):
    template_name = 'points_awarded.html'

    def get_queryset(self, pk):
        return Student.objects.get(pk=pk)

    def get(self, response, pk):
        student = self.get_queryset(pk)
        context = {'student': student}
        return self.render_to_response(context)


class PointsSwitchboardView(generic.View):
    def post(self, request, pk):
        view = AwardPointsView.as_view()
        return view(request, pk)

    def get(self, request, pk):
        view = PointsAwardedView.as_view()
        return view(request, pk)
