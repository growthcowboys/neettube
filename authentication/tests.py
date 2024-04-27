from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

# Create your tests here.

create_user_data = {
    "username":"username",
    "email":"username@example.com",
    "password":"password",
    "confirm_password": "password",
}

create_user_data_error = {
    "username":"",
    "email": "username@example.com",
    "password":"password",
    "confirm_password":"password"
}

create_user_data_passwords_error = {
    "username":"",
    "email": "username@example.com",
    "password":"password",
    "confirm_password":"different"
}


class UserViewTest(APITestCase):


    def setUp(self):

        self.client = APIClient()


    def test_create_account(self):

        url = reverse("user-list")

        response = self.client.post(url, create_user_data_error)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, create_user_data_passwords_error)

        response = self.client.post(url, create_user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().username, create_user_data["username"])
        self.assertEqual(get_user_model().objects.get().email, create_user_data["email"])


    def test_list_account(self):

        self.test_user = get_user_model().objects.create_user(
            username = create_user_data["username"],
            email = create_user_data["email"],
            password = create_user_data["password"]
        )
        
        url = reverse("user-list")

        response = self.client.get(url)

        self.assertEqual(response.data["count"], 1)

    
    def test_get_account_detail(self):

        self.test_user = get_user_model().objects.create_user(
            username = create_user_data["username"],
            email = create_user_data["email"],
            password = create_user_data["password"]
        )

        url = reverse("user-detail", args = [self.test_user.id, ])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_account_detail(self):

        updated_data = {"email": "update@example.com"}

        self.test_user = get_user_model().objects.create_user(
            username = create_user_data["username"],
            email = create_user_data["email"],
            password = create_user_data["password"]
        )

        self.test_user_two = get_user_model().objects.create_user(
            username = "username1",
            email = "email@example.com",
            password = "password"
        )


        url = reverse("user-detail", args = [self.test_user.id, ])

        response = self.client.patch(url, updated_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user = self.test_user)

        response = self.client.patch(url, updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user = self.test_user_two)

        response = self.client.patch(url, updated_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)