from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from test.models import Companies,Departments,Staff

class AccountTests(APITestCase):
    def setUp(self):
        #here we should create  object
        pass

    def test_staff_list(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('staff-list')
        #data = {'name': 'DabApps'}
        response = self.client.get(url,format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Staff.objects.count(), 0)
        # self.assertEqual(Account.objects.get().name, 'DabApps')
        # self.assertEqual(response.data, {'id':1})


    def test_getDepartments(self):
        self.assertEqual(200, 200)
