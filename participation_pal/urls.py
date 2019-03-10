from django.contrib import admin
from django.urls import path

from participation_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('student/<id>', views.student, name='student'),
    path('chosen', views.chosen, name='chosen'),
]
