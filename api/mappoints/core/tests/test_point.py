from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from mappoints.core.models import User, Point
from mappoints.core.tests import utils

class PointTest(APITestCase):
    """
    Test the actions for the Point resource in the API.
    """

    def test_user_point_retrieve(self):
        """
        Test that a single point can be retrieved under the User resource.
        Checks:
            - valid GET response status is 200
            - response data attributes match the ones sent in the request
            - creator, _url and _parent links are valid (accessible with a GET request)
            - trying to retrieve a non-existent point gives a 404
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing', latitude=12.123, longitude=45.456, creator=user)

        url = reverse('user-point-detail', args=[user.id, point.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data['description'], 'testing')
        self.assertEqual(response.data['latitude'], '12.123000')
        self.assertEqual(response.data['longitude'], '45.456000')
        self.assertTrue(utils.check_creator_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

        invalid_response = self.client.get(url + '1')
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_point_list(self):
        """
        Test that the list of points for a single user can be retrieved.
        Checks:
            - valid GET response status is 200
            - a single resource is returned in the _items attribute
            - response data attributes match the ones sent in the request
            - _url and _parent links are valid (accessible with a GET request)
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)

        url = reverse('user-point-list', args=[user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['_items']), 1)
        self.assertEqual(response.data['_items'][0]['name'], 'test')
        self.assertEqual(response.data['_items'][0]['description'], 'testing')
        self.assertEqual(response.data['_items'][0]['latitude'], '12.123000')
        self.assertEqual(response.data['_items'][0]['longitude'], '45.456000')
        self.assertTrue(utils.check_creator_get(self.client, response.data['_items'][0]))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data['_items'][0]))

    def test_point_retrieve(self):
        """
        Test that a single point can be retrieved.
        Checks:
            - valid GET response status is 200
            - response data attributes match the ones sent in the request
            - creator, _url and _parent links are valid (accessible with a GET request)
            - trying to retrieve a non-existent point gives a 404
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing', latitude=12.123, longitude=45.456, creator=user)

        url = reverse('point-detail', args=[point.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data['description'], 'testing')
        self.assertEqual(response.data['latitude'], '12.123000')
        self.assertEqual(response.data['longitude'], '45.456000')
        self.assertTrue(utils.check_creator_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

        invalid_response = self.client.get(url + '1')
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_point_list(self):
        """
        Test that the list of points can be retrieved.
        Checks:
            - valid GET response status is 200
            - a single resource is returned in the _items attribute
            - response data attributes match the ones sent in the request
            - _url and _parent links are valid (accessible with a GET request)
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)

        url = reverse('point-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['_items']), 1)
        self.assertEqual(response.data['_items'][0]['name'], 'test')
        self.assertEqual(response.data['_items'][0]['description'], 'testing')
        self.assertEqual(response.data['_items'][0]['latitude'], '12.123000')
        self.assertEqual(response.data['_items'][0]['longitude'], '45.456000')
        self.assertTrue(utils.check_creator_get(self.client, response.data['_items'][0]))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data['_items'][0]))

    def test_point_create(self):
        """
        Test that a new point can be created.
        Checks:
            - trying to create a point without authentication gives a 401
            - valid POST response status is 201
            - response data attributes match the ones sent in the request
            - creator, _url and _parent links are valid (accessible with a GET request)
            - trying to create a point with the same name by the same creator gives a 409
            - trying to create a point with an invalid latitude value gives a 400
            - trying to create a point with an invalid longitude value gives a 400
            - trying to create a point with a too big latitude value gives a 400
            - trying to create a point with a too small longitude value gives a 400
            - trying to create a point without a latitude gives a 400
            - trying to create a point without a longitude gives a 400
        """

        user = User(username='tester', location='Test')
        user.set_password('tester')
        user.save()

        data = {
            'name': 'test',
            'description': 'testing',
            'latitude': 12.123456,
            'longitude': 45.456789,
        }
        url = reverse('point-list')

        unauthorized_response = self.client.post(url, data)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester:tester'))

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data['description'], 'testing')
        self.assertEqual(response.data['latitude'], '12.123456')
        self.assertEqual(response.data['longitude'], '45.456789')
        self.assertTrue(utils.check_creator_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

        duplicate_response = self.client.post(url, data)
        self.assertEqual(duplicate_response.status_code, status.HTTP_409_CONFLICT)

        no_name_data = { 'latitude': 12.123456, 'longitude': 45.456789 }
        no_name_response = self.client.post(url, no_name_data)
        self.assertEqual(no_name_response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_latitude_data = { 'name': 'test2', 'latitude': '12.3a5', 'longitude': 45.456789 }
        invalid_latitude_response = self.client.post(url, invalid_latitude_data)
        self.assertEqual(invalid_latitude_response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_longitude_data = { 'name': 'test2', 'latitude': 12.345, 'longitude': ''}
        invalid_longitude_response = self.client.post(url, invalid_longitude_data)
        self.assertEqual(invalid_longitude_response.status_code, status.HTTP_400_BAD_REQUEST)

        # latitude larger than max (90)
        too_large_latitude_data = { 'name': 'test2', 'latitude': 90.345, 'longitude': -10}
        too_large_latitude_response = self.client.post(url, too_large_latitude_data)
        self.assertEqual(too_large_latitude_response.status_code, status.HTTP_400_BAD_REQUEST)

        # longitude smaller than min (-180)
        too_small_longitude_data = { 'name': 'test2', 'latitude': 80.345, 'longitude': -181}
        too_small_longitude_data = self.client.post(url, too_small_longitude_data)
        self.assertEqual(too_small_longitude_data.status_code, status.HTTP_400_BAD_REQUEST)

        no_latitude_data = { 'name': 'test2', 'longitude': 45.456789 }
        no_latitude_response = self.client.post(url, no_latitude_data)
        self.assertEqual(no_latitude_response.status_code, status.HTTP_400_BAD_REQUEST)

        no_longitude_data = { 'name': 'test2', 'latitude': 12.123456 }
        no_longitude_response = self.client.post(url, no_longitude_data)
        self.assertEqual(no_longitude_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_point_update(self):
        """
        Test that a point can be updated.
        Checks:
            - trying to update the point without authentication gives a 401
            - trying to update the point as a different user gives a 403
            - valid PUT response status is 200
            - trying to update the point without a latitude gives a 400
            - trying to update the point without a longitude gives a 400
            - trying to update the point with an invalid latitude gives a 400
            - trying to update the point with an invalid longitude gives a 400
        """

        user = User(username='tester', location='Test')
        user.set_password('tester')
        user.save()
        user2 = User(username='tester2', location='Test')
        user2.set_password('tester2')
        user2.save()
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)

        url = reverse('point-detail', args=[point.id])
        data = {
            'name': 'updated point',
            'description': 'hello',
            'latitude': -12.123,
            'longitude': -45.456
        }

        unauthorized_response = self.client.put(url, data)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester2:tester2'))

        forbidden_response = self.client.put(url, data)
        self.assertEqual(forbidden_response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester:tester'))

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        no_latitude_data = { 'name': 'updated point again', 'longitude': 45.456789 }
        no_latitude_response = self.client.put(url, no_latitude_data)
        self.assertEqual(no_latitude_response.status_code, status.HTTP_400_BAD_REQUEST)

        no_longitude_data = { 'name': 'updated point again', 'latitude': 12.123456 }
        no_longitude_response = self.client.put(url, no_longitude_data)
        self.assertEqual(no_longitude_response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_latitude_data = { 'name': 'update it', 'latitude': 'hello', 'longitude': 45.123 }
        invalid_latitude_response = self.client.put(url, invalid_latitude_data)
        self.assertEqual(invalid_latitude_response.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_longitude_data = { 'name': 'update it', 'latitude': 12.123, 'longitude': '0x123' }
        invalid_longitude_response = self.client.put(url, invalid_longitude_data)
        self.assertEqual(invalid_longitude_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_point_delete(self):
        """
        Test that a point can be deleted.
        Checks:
            - trying to delete the point without authentication gives a 401
            - valid DELETE response status is 204
            - trying to delete the same point again gives a 404
        """

        user = User(username='tester', location='Test')
        user.set_password('tester')
        user.save()
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)

        url = reverse('point-detail', args=[point.id])

        unauthorized_response = self.client.delete(url)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester:tester'))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        not_found_response = self.client.delete(url)
        self.assertEqual(not_found_response.status_code, status.HTTP_404_NOT_FOUND)
