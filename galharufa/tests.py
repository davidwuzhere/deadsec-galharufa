#from django.test import TestCase
import requests

# Create your tests here.

BASE_URL = "http://localhost:8000/api/v1/"

class TestUserViews:
    def test_create_user(self):
        data = {"username": "giga_chad", 
                "email": "giga_chad@test.com",
                "password": "test",
                "password2": "test",
                }
        r = requests.post(data=data, url=f"{BASE_URL}users/register")
        print(r.json())
        assert r.json() == {'username': 'giga_chad', 'email': 'giga_chad@test.com'} or r.json() == {'username': ['user com este username já existe.'], 'email': ['user com este email já existe.']}

