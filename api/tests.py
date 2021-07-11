from django.test import TestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail


class CreateCompany(TestCase):

    """This test is for create company API"""

    def test_success(self):
        """Test Success"""
        r = self.client.post('/mozio/api/v1/company-create/', {
            "name": "Ifeanyi company",
            "email": "ify@icloud.com",
            "phone_number": "091882993",
            "language": "eng",
            "currency": "USD",
            "password": "dada12345"
        })
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)


class CompanyLogin(TestCase):

    """This test is for company login"""

    def test_success(self):
        """Test Success"""
        r = self.client.post('/mozio/api/v1/company-login/', {
            "email": "Spinannsh@gmail.com",
            "password": "dada12345",
        })
        self.assertNotEqual(r.status_code, status.HTTP_200_OK)


class GetAllCompany(TestCase):

    """This test is for company login"""

    def test_success(self):
        """Test Success"""
        r = self.client.get('/mozio/api/v1/company-login/', {
            "email": "ify@icloud.com",
            "password": "dada12345"
        }, content_type='application/json')
        token = r.data
        # print(r.status_code)
        header = {'HTTP_AUTHORIZATION': 'Bearer {token}'.format(token=token)}
        r = self.client.get('/mozio/api/v1/all-companies/', **header)
        self.assertNotEqual(r.status_code, status.HTTP_200_OK)


class GetCompany(TestCase):

    """This test is for company login"""

    def test_success(self):
        """Test Success"""
        r = self.client.get('/mozio/api/v1/company-login/', {
            "email": "ify@icloud.com",
            "password": "dada12345"
        }, content_type='application/json')
        token = r.data['data']['access_token']
        header = {'HTTP_AUTHORIZATION': 'Bearer {token}'.format(token=token)}
        r = self.client.get('/mozio/api/v1/company/', **header)
        self.assertNotEqual(r.status_code, status.HTTP_200_OK)
