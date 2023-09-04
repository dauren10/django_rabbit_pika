from django.urls import path
from .views import TestListView,SampleListView,ConsListView

urlpatterns = [
    path('test', TestListView.as_view(), name='test'),
    path('sample', SampleListView.as_view(), name='sample'),
    path('cons', ConsListView.as_view(), name='cons'),
]