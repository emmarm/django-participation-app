from django.contrib import admin
from django.urls import path

from participation_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/<id>', views.student, name='student')
]
