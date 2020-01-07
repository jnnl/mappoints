from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from mappoints.core.models import User, Point, Comment, Tag, Star

from decimal import Decimal

class UserTest(TestCase):
    """
    Test the create, read, update and delete operations on User models.
    Also check that constraints and restrictions are enforced.
    """

    def setUp(self):
        user = User(username='tester', location='Canberra')
        user.set_password('tester')
        user.save()

    def test_user_create(self):
        """
        Test that a user can be created properly (every attribute matches).
        """

        user = User(username='new_user', location='Perth')
        user.set_password('new_user')
        user.save()

        self.assertEqual(User.objects.filter(username='new_user', location='Perth').exists(), True)
        self.assertEqual(len(User.objects.all()), 2)

    def test_user_retrieve(self):
        """
        Test that a single user matching the filter can be retrieved.
        """

        self.assertEqual(User.objects.filter(username='tester', location='Canberra').exists(), True)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(User.objects.filter(username='new_user', location='Perth').exists(), False)

    def test_user_list(self):
        """
        Test that all users can be listed (length should be 1).
        """

        self.assertEqual(len(User.objects.all()), 1)

    def test_user_update(self):
        """
        Test that the user can be updated (changed attributes should be saved).
        """

        user = User.objects.first()
        user.username = 'updated_user'
        user.location = 'Sydney'
        user.save(update_fields=['username', 'location'])

        updated_user = User.objects.first()
        self.assertEqual(updated_user.username, 'updated_user')
        self.assertEqual(updated_user.location, 'Sydney')

    def test_user_delete(self):
        """
        Test that a single user can be deleted.
        """

        user = User.objects.first()
        user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get()

        users = User.objects.all()
        self.assertEqual(len(users), 0)

    def test_user_delete_all(self):
        """
        Test that all users can be deleted (length should be 0).
        """

        users = User.objects.all()
        self.assertEqual(len(users), 1)
        users.delete()
        self.assertEqual(len(users), 0)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get()

    def test_user_unique(self):
        """
        Test that the unique constraint for users is enforced (has to raise IntegrityError).
        """

        user = User.objects.get(username='tester')
        with self.assertRaises(IntegrityError):
            User.objects.create(username='tester', password='tester', location='Canberra')

class PointTest(TestCase):
    """
    Test the create, read, update and delete operations on Point models.
    Also check that constraints and restrictions are enforced.
    """

    def setUp(self):
        user = User.objects.create(username='tester', password='tester')
        Point.objects.create(
            name='Brisbane',
            latitude=-27.466667,
            longitude=153.033333,
            description='Capital of Queensland.',
            creator=user
        )

    def match_original_point(self, point):
        """
        Ensure the point matches the originally created point.

        The assertAlmostEqual method is used to compare latitude and longitude
        because it rounds to 7 places which is accurate enough for the requirements.
        """

        user = User.objects.first()
        self.assertEqual(point.name, 'Brisbane')
        self.assertAlmostEqual(point.latitude, Decimal(-27.466667))
        self.assertAlmostEqual(point.longitude, Decimal(153.033333))
        self.assertEqual(point.description, 'Capital of Queensland.')
        self.assertEqual(point.creator.id, user.id)

    def test_point_create(self):
        """
        Test that a single point is created properly (every attribute matches).
        """

        user = User.objects.first()
        point = Point.objects.create(
            name='Melbourne',
            latitude=-37.813611,
            longitude=144.963056,
            description='Capital of Victoria.',
            creator=user
        )

        point = Point.objects.get(name='Melbourne', creator=user)

        self.assertEqual(point.name, 'Melbourne')
        self.assertAlmostEqual(point.latitude, Decimal(-37.813611))
        self.assertAlmostEqual(point.longitude, Decimal(144.963056))
        self.assertEqual(point.description, 'Capital of Victoria.')
        self.assertEqual(point.creator.id, user.id)

    def test_point_retrieve(self):
        """
        Test that a point matching a filter can be retrieved.
        """

        point = Point.objects.get(name='Brisbane')
        self.match_original_point(point)
        self.assertEqual(Point.objects.filter(name='Brisbane').exists(), True)
        self.assertEqual(Point.objects.filter(name='Perth').exists(), False)

    def test_point_list(self):
        """
        Test that all points can be listed (length should be 1).
        """

        points = Point.objects.all()
        self.assertEqual(len(points), 1)

    def test_point_update(self):
        """
        Test that the point can be updated (changed attributes should be saved).
        """

        point = Point.objects.first()
        point.name = 'Sydney'
        point.latitude = -33.865
        point.longitude = 151.209444
        point.description = 'Capital of New South Wales.'
        point.save(update_fields=['name', 'latitude', 'longitude', 'description'])

        updated_point = Point.objects.first()
        self.assertEqual(updated_point.name, 'Sydney')
        self.assertAlmostEqual(updated_point.latitude, Decimal(-33.865))
        self.assertAlmostEqual(updated_point.longitude, Decimal(151.209444))
        self.assertEqual(updated_point.description, 'Capital of New South Wales.')

    def test_point_delete(self):
        """
        Test that a single point can be deleted.
        """

        point = Point.objects.first()
        point.delete()
        with self.assertRaises(Point.DoesNotExist):
            Point.objects.get()

        points = Point.objects.all()
        self.assertEqual(len(points), 0)

    def test_point_delete_all(self):
        """
        Test that all points can be deleted (length should be 0).
        """

        points = Point.objects.all()
        self.assertEqual(len(points), 1)
        points.delete()
        self.assertEqual(len(points), 0)
        with self.assertRaises(Point.DoesNotExist):
            Point.objects.get()

    def test_point_create_no_creator(self):
        """
        Test that a point cannot be created without a creator (NOT NULL is enforced).
        """
        user = User.objects.first()
        with self.assertRaises(IntegrityError):
            Point.objects.create(name='point', latitude=0, longitude=0)

    def test_point_ondelete(self):
        """
        Test that a point is deleted if its creator is deleted (on_delete should CASCADE).
        """

        point = Point.objects.first()
        point.creator.delete()

        with self.assertRaises(Point.DoesNotExist):
            Point.objects.get()

    def test_point_unique(self):
        """
        Test that the unique constraint for points is enforced (has to raise IntegrityError).
        """

        user = User.objects.get(username='tester')
        with self.assertRaises(IntegrityError):
            Point.objects.create(
                name='Brisbane',
                latitude=12.12345,
                longitude=12.12345,
                description='',
                creator=user
            )

    def test_point_latitude_range(self):
        """
        Test that the latitude min and max value validators are enforced
        (-90 <= longitude <= 90).
        """

        user = User.objects.get(username='tester')
        point = Point(
            name='test point',
            latitude=90,
            longitude=0.0,
            description='',
            creator=user
        )
        point.full_clean()
        point.latitude = -90
        point.full_clean()

        with self.assertRaises(ValidationError):
            point.latitude = -91
            point.full_clean()

        with self.assertRaises(ValidationError):
            point.latitude = 90.00001
            point.full_clean()

    def test_point_longitude_range(self):
        """
        Test that the longitude min and max value validators are enforced
        (-180 <= longitude <= 180).
        """

        user = User.objects.get(username='tester')
        point = Point(
            name='test point',
            latitude=0.0,
            longitude=180,
            description='',
            creator=user
        )
        point.full_clean()
        point.longitude = -180
        point.full_clean()

        with self.assertRaises(ValidationError):
            point.longitude = -181
            point.full_clean()

        with self.assertRaises(ValidationError):
            point.longitude = 180.00001
            point.full_clean()

class CommentTest(TestCase):
    """
    Test the create, read, update and delete operations on Comment models.
    Also check that constraints and restrictions are enforced.
    """

    def setUp(self):
        user = User.objects.create(username='tester', password='tester')
        point = Point.objects.create(
            name='Melbourne',
            latitude=-37.813611,
            longitude=144.963056,
            description='Capital of Victoria.',
            creator=user
        )
        Comment.objects.create(content='hello world', creator=user, point=point)

    def test_comment_create(self):
        """
        Test that a single comment is created properly (every attribute matches).
        """
        user = User.objects.first()
        point = Point.objects.first()
        comment = Comment.objects.create(content='created comment', creator=user, point=point)

        self.assertEqual(Comment.objects.filter(content='created comment', creator=user, point=point).exists(), True)

    def test_comment_create_no_creator(self):
        """
        Test that a comment cannot be created without a creator (NOT NULL is enforced).
        """
        point = Point.objects.first()
        with self.assertRaises(IntegrityError):
            Comment.objects.create(content='created comment', point=point)

    def test_comment_create_no_point(self):
        """
        Test that a comment cannot be created without a point (NOT NULL is enforced).
        """
        user = User.objects.first()
        with self.assertRaises(IntegrityError):
            Comment.objects.create(content='created comment', creator=user)

    def test_comment_retrieve(self):
        """
        Test that a comment matching a filter can be retrieved.
        """

        Comment.objects.get(content='hello world')
        self.assertEqual(Comment.objects.filter(content='hello world').exists(), True)

    def test_comment_update(self):
        """
        Test that the comment can be updated (changed attributes should be saved).
        """
        comment = Comment.objects.first()
        comment.content = 'hola mundo'
        comment.save()

        self.assertEquals(Comment.objects.filter(content='hola mundo').exists(), True)
        self.assertEquals(Comment.objects.filter(content='hello world').exists(), False)

    def test_comment_delete(self):
        """
        Test that a single comment can be deleted (should no longer exist).
        """
        comment = Comment.objects.first()
        comment.delete()

        self.assertEquals(len(Comment.objects.all()), 0)

    def test_point_ondelete_creator(self):
        """
        Test that a comment is deleted if its creator is deleted (on_delete should CASCADE).
        """

        comment = Comment.objects.first()
        comment.creator.delete()

        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get()

    def test_point_ondelete_point(self):
        """
        Test that a comment is deleted if its point is deleted (on_delete should CASCADE).
        """

        comment = Comment.objects.first()
        comment.point.delete()

        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get()

class TagTest(TestCase):
    """
    Test the create, read, update and delete operations on Tag models.
    Also check that constraints and restrictions are enforced.
    """

    def setUp(self):
        user = User.objects.create(username='tester', password='tester')
        point = Point.objects.create(
            name='Melbourne',
            latitude=-37.813611,
            longitude=144.963056,
            description='Capital of Victoria.',
            creator=user
        )
        Tag.objects.create(name='tag', creator=user, point=point)

    def test_tag_create(self):
        """
        Test that a single tag is created properly (every attribute matches).
        """
        user = User.objects.first()
        point = Point.objects.first()
        tag = Tag.objects.create(name='created tag', creator=user, point=point)

        self.assertEqual(Tag.objects.filter(name='created tag', creator=user, point=point).exists(), True)

    def test_tag_create_no_creator(self):
        """
        Test that a tag cannot be created without a creator (NOT NULL is enforced).
        """
        point = Point.objects.first()
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name='created tag', point=point)

    def test_tag_create_no_point(self):
        """
        Test that a tag cannot be created without a point (NOT NULL is enforced).
        """
        user = User.objects.first()
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name='created tag', creator=user)

    def test_tag_retrieve(self):
        """
        Test that a tag matching a filter can be retrieved.
        """

        Tag.objects.get(name='tag')
        self.assertEqual(Tag.objects.filter(name='tag').exists(), True)

    def test_tag_update(self):
        """
        Test that the tag can be updated (changed attributes should be saved).
        """
        tag = Tag.objects.first()
        tag.name = 'updated tag'
        tag.save()

        self.assertEquals(Tag.objects.filter(name='updated tag').exists(), True)
        self.assertEquals(Tag.objects.filter(name='tag').exists(), False)

    def test_tag_delete(self):
        """
        Test that a single tag can be deleted (should no longer exist).
        """
        tag = Tag.objects.first()
        tag.delete()

        self.assertEquals(len(Tag.objects.all()), 0)

    def test_tag_ondelete_creator(self):
        """
        Test that a tag is deleted if its creator is deleted (on_delete should CASCADE).
        """

        tag = Tag.objects.first()
        tag.creator.delete()

        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get()

    def test_tag_ondelete_point(self):
        """
        Test that a tag is deleted if its point is deleted (on_delete should CASCADE).
        """

        tag = Tag.objects.first()
        tag.point.delete()

        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get()

    def test_tag_unique(self):
        """
        Test that the unique constraint for tags is enforced (has to raise IntegrityError).
        """

        tag = Tag.objects.first()
        user = User.objects.first()
        point = Point.objects.first()

        with self.assertRaises(IntegrityError):
            Tag.objects.create(name='tag', creator=user, point=point)

class StarTest(TestCase):
    """
    Test the create, read, update and delete operations on Star models.
    Also check that constraints and restrictions are enforced.
    """

    def setUp(self):
        user = User.objects.create(username='tester', password='tester')
        point = Point.objects.create(
            name='Melbourne',
            latitude=-37.813611,
            longitude=144.963056,
            description='Capital of Victoria.',
            creator=user
        )
        Star.objects.create(creator=user, point=point)

    def test_star_create(self):
        """
        Test that a single star is created properly (every attribute matches).
        """
        user = User.objects.first()
        point = Point.objects.first()
        Star.objects.all().delete()
        star = Star.objects.create(creator=user, point=point)

        self.assertEqual(Star.objects.filter(creator=user, point=point).exists(), True)

    def test_star_create_no_creator(self):
        """
        Test that a star cannot be created without a creator (NOT NULL is enforced).
        """
        point = Point.objects.first()
        with self.assertRaises(IntegrityError):
            Star.objects.create(point=point)

    def test_star_create_no_point(self):
        """
        Test that a star cannot be created without a point (NOT NULL is enforced).
        """
        user = User.objects.first()
        with self.assertRaises(IntegrityError):
            Star.objects.create(creator=user)

    def test_star_retrieve(self):
        """
        Test that a star matching a filter can be retrieved.
        """

        user = User.objects.first()
        point = Point.objects.first()
        Star.objects.get(creator=user, point=point)
        self.assertEqual(Star.objects.filter(creator=user, point=point).exists(), True)

    def test_star_delete(self):
        """
        Test that a single star can be deleted (should no longer exist).
        """
        star = Star.objects.first()
        star.delete()

        self.assertEquals(len(Star.objects.all()), 0)

    def test_star_ondelete_creator(self):
        """
        Test that a star is deleted if its creator is deleted (on_delete should CASCADE).
        """

        star = Star.objects.first()
        star.creator.delete()

        with self.assertRaises(Star.DoesNotExist):
            Star.objects.get()

    def test_star_ondelete_point(self):
        """
        Test that a star is deleted if its point is deleted (on_delete should CASCADE).
        """

        star = Star.objects.first()
        star.point.delete()

        with self.assertRaises(Star.DoesNotExist):
            Star.objects.get()

    def test_star_unique(self):
        """
        Test that the unique constraint for stars is enforced (has to raise IntegrityError).
        """

        star = Star.objects.first()
        user = User.objects.first()
        point = Point.objects.first()

        with self.assertRaises(IntegrityError):
            Star.objects.create(creator=user, point=point)
