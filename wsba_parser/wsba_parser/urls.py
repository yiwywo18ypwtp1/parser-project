from django.contrib import admin
from django.urls import path

from parser_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('parse_member/', views.parse_members, name='parse_members'),
    path('parse_results/', views.parse_results, name='parse_results')
]
