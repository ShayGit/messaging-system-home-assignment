from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class UserSignUpTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.messages_url = reverse('messages-list')
        cls.client = APIClient()
        cls.user1data = {
            "username": "user1",
            "password": "123456"
        }
        cls.user2data = {
            "username": "user2",
            "password": "123456"
        }
        res = cls.client.post(reverse('signup'), cls.user1data, format="json")
        cls.user1token = cls.existing_user_access_data = res.data['tokens']['access']

        res = cls.client.post(reverse('signup'), cls.user2data, format="json")
        cls.user2token = cls.existing_user_access_data = res.data['tokens']['access']

        # Send 1 message from user 1 to user 2
        message = {
            "receiver": "user2",
            "subject": "message from user1 to user2",
            "message": "this is my message to user2"
        }
        res = cls.client.post(cls.messages_url, message, format="json",
                              HTTP_AUTHORIZATION='Bearer ' + cls.user1token)
        cls.user1_sent_message = res.data

        # Send some messages from user 2 to user1
        cls.user1_received_messages = []

        for i in range(1, 5):
            message = {
                "receiver": "user1",
                "subject": f"message:{i} from user2 to user1",
                "message": f"this is my message{i} to user1"
            }
            res = cls.client.post(cls.messages_url, message, format="json",
                                  HTTP_AUTHORIZATION='Bearer ' + cls.user2token)
            cls.user1_received_messages.append(res.data)

        # Read first message
        cls.client.get(cls.messages_url + f"{cls.user1_received_messages[0]['id']}/", format="json",
                       HTTP_AUTHORIZATION='Bearer ' + cls.user1token)
        cls.user1_received_messages[0]['is_read'] = True

    def test_user_can_add_message(self):
        message = {
            "receiver": "user2",
            "subject": "message from user1 to user2",
            "message": "this is my message to user2"
        }
        res = self.client.post(self.messages_url, message, format="json",
                               HTTP_AUTHORIZATION='Bearer ' + self.user1token)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            res.data,
            {
                "id": res.data["id"],
                "sender": "user1",
                "receiver": "user2",
                "subject": "message from user1 to user2",
                "message": "this is my message to user2",
                "is_read": False,
                "creation_date": res.data["creation_date"]
            }
        )

    def test_user_can_get_all_messages(self):
        res = self.client.get(self.messages_url, format="json", HTTP_AUTHORIZATION='Bearer ' + self.user1token)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            self.user1_received_messages
        )

    def test_user_can_read_message(self):
        res = self.client.get(self.messages_url + f"{self.user1_received_messages[0]['id']}/", format="json",
                              HTTP_AUTHORIZATION='Bearer ' + self.user1token)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            self.user1_received_messages[0]
        )

    def test_user_can_get_unread_messages(self):
        res = self.client.get(self.messages_url + "?is_read=false", format="json",
                              HTTP_AUTHORIZATION='Bearer ' + self.user1token)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            self.user1_received_messages[1:]
        )

    def test_user_can_delete_received_message(self):
        res = self.client.delete(self.messages_url + f"{self.user1_received_messages[0]['id']}/", format="json",
                                 HTTP_AUTHORIZATION='Bearer ' + self.user1token)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_can_delete_sent_message(self):
        res = self.client.delete(self.messages_url + f"{self.user1_sent_message['id']}/", format="json",
                                 HTTP_AUTHORIZATION='Bearer ' + self.user1token)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
