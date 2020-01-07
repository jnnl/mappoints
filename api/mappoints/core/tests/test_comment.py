from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from mappoints.core.models import User, Point, Comment, Tag, Star
from mappoints.core.tests import utils

class CommentTest(APITestCase):
    """
    Test the actions for the Comment resource in the API.
    """

    def test_comment_retrieve(self):
        """
        Test that a single comment can be retrieved.
        Checks:
            - valid GET response status is 200
            - response data attributes match the ones sent in the request
            - creator, point, _url and _parent links are valid (accessible with a GET request)
            - trying to retrieve a non-existent comment gives a 404
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing', latitude=12.123, longitude=45.456, creator=user)
        comment = Comment.objects.create(content='hello world', creator=user, point=point)

        url = reverse('point-comment-detail', args=[point.id, comment.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'hello world')
        self.assertTrue(utils.check_creator_get(self.client, response.data))
        self.assertTrue(utils.check_point_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

        invalid_response = self.client.get(url + '1')
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_list(self):
        """
        Test that the list of comments for a point can be retrieved.
        Checks:
            - valid GET response status is 200
            - a single resource is returned in the _items attribute
            - response data attributes match the ones sent in the request
            - creator, point, _url and _parent links are valid (accessible with a GET request)
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)
        comment = Comment.objects.create(content='hello world', creator=user, point=point)

        url = reverse('point-comment-list', args=[point.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['_items']), 1)
        self.assertEqual(response.data['_items'][0]['content'], 'hello world')
        self.assertTrue(utils.check_point_get(self.client, response.data['_items'][0]))
        self.assertTrue(utils.check_creator_get(self.client, response.data['_items'][0]))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data['_items'][0]))

    def test_comment_create(self):
        """
        Test that a new comment for a point can be created.
        Checks:
            - trying to create a comment without authentication gives a 401
            - valid POST response status is 201
            - response data attributes match the ones sent in the request
            - creator, point, _url and _parent links are valid (accessible with a GET request)
        """

        user = User(username='tester', location='Test')
        user.set_password('tester')
        user.save()
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)

        data = {
            'content': 'A new comment.',
        }
        url = reverse('point-comment-list', args=[point.id])

        unauthorized_response = self.client.post(url, data)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester:tester'))

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'A new comment.')
        self.assertTrue(utils.check_point_get(self.client, response.data))
        self.assertTrue(utils.check_creator_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

    def test_comment_update(self):
        """
        Test that a comment can be updated.
        Checks:
            - trying to update the comment without authentication gives a 401
            - trying to update the comment as a different user gives a 403
            - valid PUT response status is 200
        """

        user = User(username='tester', location='Test')
        user.set_password('tester')
        user.save()
        user2 = User(username='tester2', location='Test')
        user2.set_password('tester2')
        user2.save()
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)
        comment = Comment.objects.create(content='hello world', creator=user, point=point)

        url = reverse('point-comment-detail', args=[point.id, comment.id])
        data = {
            'content': 'updated comment',
        }

        unauthorized_response = self.client.put(url, data)
        self.assertEqual(unauthorized_response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester2:tester2'))

        forbidden_response = self.client.put(url, data)
        self.assertEqual(forbidden_response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION=utils.get_basic_auth_header('tester:tester'))

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_delete(self):
        """
        Test that a comment can be deleted.
        Checks:
            - trying to delete the comment without authentication gives a 401
            - trying to delete the comment as a different user gives a 403
            - valid DELETE response status is 204
            - trying to delete the same comment again gives a 404
        """

        user = User(username='tester', location='Test')
        user.set_password('tester')
        user.save()
        user2 = User(username='tester2', location='Test')
        user2.set_password('tester2')
        user2.save()
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)
        comment = Comment.objects.create(content='hello world', creator=user, point=point)

        url = reverse('point-comment-detail', args=[point.id, comment.id])

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

    def test_user_comment_retrieve(self):
        """
        Test that a single comment by a user can be retrieved.
        Checks:
            - valid GET response status is 200
            - response data attributes match the ones sent in the request
            - creator, point, _url and _parent links are valid (accessible with a GET request)
            - trying to retrieve a non-existent comment gives a 404
            - trying to retrieve a comment for a non-existent user gives a 404
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing', latitude=12.123, longitude=45.456, creator=user)
        comment = Comment.objects.create(content='hello world', creator=user, point=point)

        url = reverse('user-comment-detail', args=[user.id, comment.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'hello world')
        self.assertTrue(utils.check_creator_get(self.client, response.data))
        self.assertTrue(utils.check_point_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))

        invalid_response = self.client.get(url + '1')
        self.assertEqual(invalid_response.status_code, status.HTTP_404_NOT_FOUND)

        invalid_user_url = reverse('user-comment-detail', args=[0, comment.id])
        invalid_user_response = self.client.get(invalid_user_url)
        self.assertEqual(invalid_user_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_comment_list(self):
        """
        Test that the list of comments by a user can be retrieved.
        Checks:
            - valid GET response status is 200
            - a single resource is returned in the _items attribute
            - response data attributes match the ones sent in the request
            - creator, point, _url and _parent links are valid (accessible with a GET request)
            - trying to retrieve comments for a non-existent user gives a 404
        """

        user = User.objects.create(username='tester', password='tester', location='Test')
        point = Point.objects.create(name='test', description='testing',
                                     latitude=12.123, longitude=45.456, creator=user)
        comment = Comment.objects.create(content='hello world', creator=user, point=point)

        url = reverse('user-comment-list', args=[user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['_items']), 1)
        self.assertEqual(response.data['_items'][0]['content'], 'hello world')
        self.assertTrue(utils.check_point_get(self.client, response.data['_items'][0]))
        self.assertTrue(utils.check_creator_get(self.client, response.data['_items'][0]))
        self.assertTrue(utils.check_url_get(self.client, response.data))
        self.assertTrue(utils.check_parent_get(self.client, response.data))
        self.assertTrue(utils.check_url_get(self.client, response.data['_items'][0]))

        invalid_user_url = reverse('user-comment-list', args=[0])
        invalid_user_response = self.client.get(invalid_user_url)
        self.assertEqual(invalid_user_response.status_code, status.HTTP_404_NOT_FOUND)
