from django.urls import path
from .views import TestListView

urlpatterns = [
    path('test', TestListView.as_view(),name='test'),
]