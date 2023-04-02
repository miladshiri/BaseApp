from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

class AccountsTestCase(APITestCase):

    register_url = "/user/register/"
    verify_email_url = "/api/auth/register/verify-email/"
    login_url = "/user/token/"

    def test_register(self):

        # register data
        data = {
            "email": "user2@example-email.com",
            "username": "user2@example-email.com",
            "password": "V1erysecret",
            "password2": "V1erysecret",
            "first_name": "myname",
            "last_name": "mylast",
        }
        # send POST request to "/api/auth/register/"
        response = self.client.post(self.register_url, data)
        # check the response status and data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["message"], "user registered successfully")


        # try to login - should fail, because email is not verified
        login_data = {
            "username": data["email"],
            "password": data["password"],
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            "E-mail is not verified." in response.json()["non_field_errors"]
        )

        # expected one email to be send
        # parse email to get token
        self.assertEqual(len(mail.outbox), 1)
        email_lines = mail.outbox[0].body.splitlines()
        activation_line = [l for l in email_lines if "verify-email" in l][0]
        activation_link = activation_line.split("go to ")[1]
        activation_key = activation_link.split("/")[4]
