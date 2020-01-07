from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from mappoints.core.models import User
from mappoints.core.tests import utils

class UserTest(APITestCase):
    """
    Test the actions for the User resource in the API.
    """

    def test_user_retrieve(self):
        """
        Test that a single user can be retrieved.
        Checks:
            - valid GET response status is 200
            - response data attributes match the ones sent in the request
            - _url and _parent links are valid (accessible with a GET request)
            - trying to retrieve a non-existent user gives a 404
        """

        user = User.objects.create(username='tester', password='tester', location='Test')

        url = reverse('user-detail', args=[user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'tester')
        self.assertEqual(response.data['location'], 'Test')
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

        invalid_response = self.client.get(url + '1')
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_list(self):
        """
        Test that the list of users can be retrieved.
        Checks:
            - valid GET response status is 200
            - a single resource is returned in the _items attribute
            - response data attributes match the ones sent in the request
            - _url and _parent links are valid (accessible with a GET request)
        """

        user = User.objects.create(username='tester', password='tester', location='Test')

        url = reverse('user-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['_items']), 1)
        self.assertEqual(response.data['_items'][0]['username'], 'tester')
        self.assertEqual(response.data['_items'][0]['location'], 'Test')
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

    def test_user_create(self):
        """
        Test that a new user can be created.
        Checks:
            - valid POST response status is 201
            - response data attributes match the ones sent in the request
            - _url and _parent links are valid (accessible with a GET request)
            - trying to create a user with the same name gives a 409
            - trying to create a user without a username gives a 400
            - trying to create a user without a password gives a 400
        """

        url = reverse('user-list')
        data = {
            'username': 'tester',
            'password': 'tester',
            'location': 'Oulu'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'tester')
        self.assertEqual(response.data['location'], 'Oulu')
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

        duplicate_response = self.client.post(url, data)
        self.assertEqual(duplicate_response.status_code, status.HTTP_409_CONFLICT)

        no_username_data = {'password': 'tester'}
        no_username_response = self.client.post(url, no_username_data)
        self.assertEqual(no_username_response.status_code, status.HTTP_400_BAD_REQUEST)

        no_password_data = {'username': 'tester2'}
        no_password_response = self.client.post(url, no_password_data)
        self.assertEqual(no_password_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_update(self):
        """
        Test that a user can be updated.
        Checks:
            - valid PUT response status is 200
            - response data attributes match the ones sent in the request
            - _url and _parent links are valid (accessible with a GET request)
            - trying to update a username with the same name gives a 403
            - trying to update a user without a username gives a 400
            - trying to update a user without a password gives a 400
        """
        user = User(username='original', location='Original')
        user.set_password('original')
        user.save()

        user2 = User(username='tester', location='Test')
        user2.set_password('tester')
        user2.save()

        url = reverse('user-detail', args=[user2.id])
        data = {
            'username': 'tester2',
            'password': 'tester2',
            'location': 'Oulu'
        }

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester:tester'))

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'tester2')
        self.assertEqual(response.data['location'], 'Oulu')

        # update user authentication details
        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester2:tester2'))

        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

        existing_user_url = reverse('user-detail', args=[user.id])
        existing_user_data = {
            'username': 'original',
            'password': 'original',
            'location': 'Oulu'
        }
        existing_user_response = self.client.put(existing_user_url, existing_user_data)
        self.assertEqual(existing_user_response.status_code, status.HTTP_403_FORBIDDEN)

        no_username_data = {'password': 'tester2'}
        no_username_response = self.client.put(url, no_username_data)
        self.assertEqual(no_username_response.status_code, status.HTTP_400_BAD_REQUEST)

        no_password_data = {'username': 'tester2'}
        no_password_response = self.client.put(url, no_password_data)
        self.assertEqual(no_password_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_delete(self):
        """
        Test that a user can be deleted.
        Checks:
            - trying to delete the user without authentication gives a 401
            - trying to delete the user as another user gives a 403
            - trying to delete a non-existing user gives a 404
            - valid DELETE response status is 204
            - trying to delete the same user again gives a 401
              (as the user is deleted and no longer authenticated)
        """

        user = User(username='tester', location='Test')
        user.set_password('tester')
        user.save()
        another_user = User(username='tester2', location='Test2')
        another_user.set_password('tester2')
        another_user.save()

        url = reverse('user-detail', args=[user.id])

        unauthorized_response = self.client.delete(url)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester2:tester2'))

        forbidden_response = self.client.delete(url)
        self.assertEqual(forbidden_response.status_code, status.HTTP_403_FORBIDDEN)

        not_found_response = self.client.delete(url + '1')
        self.assertEqual(not_found_response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester:tester'))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        deleted_response = self.client.delete(url)
        self.assertEqual(deleted_response.status_code, status.HTTP_401_UNAUTHORIZED)
