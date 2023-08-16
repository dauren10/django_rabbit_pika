from rest_framework.views import APIView
import pika
import uuid
from rest_framework.response import Response
class TestListView(APIView):
    def get(self, request, format=None):
        

        return Response('Hello')

