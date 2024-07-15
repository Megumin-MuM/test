from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('details/<int:book_id>/', views.details, name='details'),
    path('chapter/<int:chapter_id>/', views.chapter, name='chapter'),
]
