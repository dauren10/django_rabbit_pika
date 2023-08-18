from django.urls import path
from .views import TestListView,SampleListView

urlpatterns = [
    path('test', TestListView.as_view(), name='test'),
    path('sample', SampleListView.as_view(), name='sample'),
]