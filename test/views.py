from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import add
from time import sleep
class TestListView(APIView):
    def get(self,format=None):
        
        result = add.delay(4,4)
        return Response('Hello')
