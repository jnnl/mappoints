from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from mappoints.core.models import User, Point, Star
from mappoints.core.tests import utils

class StarTest(APITestCase):
    """
    Test the actions for the Star resource in the API.
    """

    def test_star_retrieve(self):
        """
        Test that a single star can be retrieved.
        Checks:
            - valid GET response status is 200
            - response data attributes match the ones sent in the request
            - creator, point, _url and _parent links are valid (accessible with a GET request)
            - trying to retrieve a non-existent star gives a 404
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing', latitude=12.123, longitude=45.456, creator=user)
        star = Star.objects.create(creator=user, point=point)

        url = reverse('point-star-detail', args=[point.id, star.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(utils.check_creator_get(self.client, response.data))
        self.assertTrue(utils.check_point_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

        invalid_response = self.client.get(url + '1')
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_star_list(self):
        """
        Test that the list of stars for a point can be retrieved.
        Checks:
            - valid GET response status is 200
            - a single resource is returned in the _items attribute
            - response data attributes match the ones sent in the request
            - creator, point, _url and _parent links are valid (accessible with a GET request)
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)
        star = Star.objects.create(creator=user, point=point)

        url = reverse('point-star-list', args=[star.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['_items']), 1)
        self.assertTrue(utils.check_point_get(self.client, response.data['_items'][0]))
        self.assertTrue(utils.check_creator_get(self.client, response.data['_items'][0]))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data['_items'][0]))

    def test_star_create(self):
        """
        Test that a new star for a point can be created.
        Checks:
            - trying to create a star without authentication gives a 401
            - valid POST response status is 201
            - response data attributes match the ones sent in the request
            - creator, point, _url and _parent links are valid (accessible with a GET request)
            - trying to create a star twice as the same user gives a 409
        """

        user = User(username='tester', location='Test')
        user.set_password('tester')
        user.save()
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)

        url = reverse('point-star-list', args=[point.id])

        unauthorized_response = self.client.post(url)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester:tester'))

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(utils.check_point_get(self.client, response.data))
        self.assertTrue(utils.check_creator_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

        duplicate_response = self.client.post(url)
        self.assertEqual(duplicate_response.status_code, status.HTTP_409_CONFLICT)

    def test_star_delete(self):
        """
        Test that a star can be deleted.
        Checks:
            - trying to delete the star without authentication gives a 401
            - trying to delete the star as a different user gives a 403
            - valid DELETE response status is 204
            - trying to delete the same star again gives a 404
        """

        user = User(username='tester', location='Test')
        user.set_password('tester')
        user.save()
        user2 = User(username='tester2', location='Test')
        user2.set_password('tester2')
        user2.save()
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)
        star = Star.objects.create(creator=user, point=point)

        url = reverse('point-star-detail', args=[point.id, star.id])

        unauthorized_response = self.client.delete(url)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester2:tester2'))

        forbidden_response = self.client.delete(url)
        self.assertEqual(forbidden_response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester:tester'))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        not_found_response = self.client.delete(url)
        self.assertEqual(not_found_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_star_retrieve(self):
        """
        Test that a single star for a user can be retrieved.
        Checks:
            - valid GET response status is 200
            - response data attributes match the ones sent in the request
            - creator, point, _url and _parent links are valid (accessible with a GET request)
            - trying to retrieve a non-existent star gives a 404
            - trying to retrieve a star for a non-existent user gives a 404
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing', latitude=12.123, longitude=45.456, creator=user)
        star = Star.objects.create(creator=user, point=point)

        url = reverse('user-star-detail', args=[user.id, star.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(utils.check_creator_get(self.client, response.data))
        self.assertTrue(utils.check_point_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

        invalid_response = self.client.get(url + '1')
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

        invalid_user_url = reverse('user-star-detail', args=[0, star.id])
        invalid_user_response = self.client.get(invalid_user_url)
        self.assertEqual(invalid_user_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_star_list(self):
        """
        Test that the list of stars by a user can be retrieved.
        Checks:
            - valid GET response status is 200
            - a single resource is returned in the _items attribute
            - response data attributes match the ones sent in the request
            - creator, point, _url and _parent links are valid (accessible with a GET request)
            - trying to retrieve stars for a non-existent user gives a 404
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)
        star = Star.objects.create(creator=user, point=point)

        url = reverse('user-star-list', args=[user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['_items']), 1)
        self.assertTrue(utils.check_point_get(self.client, response.data['_items'][0]))
        self.assertTrue(utils.check_creator_get(self.client, response.data['_items'][0]))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data['_items'][0]))

        invalid_user_url = reverse('user-star-list', args=[0])
        invalid_user_response = self.client.get(invalid_user_url)
        self.assertEqual(invalid_user_response.status_code, status.HTTP_404_NOT_FOUND)
