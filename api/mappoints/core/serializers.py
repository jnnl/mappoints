from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from mappoints.core.models import User, Point, Tag, Comment, Star
from mappoints.core.utils import get_url, get_parent_url, wrap_url

class CreatorSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Serialize and deserialize a User as a 'creator' field for other resources.
    """

    class Meta:
        model = User
        fields = ('_url', 'id', 'username')

class CommentSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Serializes and deserializes a Comment.
    Validates each deserialized field.
    """

    _url = NestedHyperlinkedIdentityField(
        read_only=True,
        view_name='point-comment-detail',
        parent_lookup_kwargs={'point_pk': 'point__pk'}
    )
    point = wrap_url(serializers.HyperlinkedRelatedField)(read_only=True, view_name='point-detail')
    creator = wrap_url(serializers.HyperlinkedRelatedField)(read_only=True, view_name='user-detail')

    class Meta:
       model = Comment
       fields = ('_url', 'id', 'content', 'created', 'point', 'creator')

    expandable_fields = {
        'creator': (CreatorSerializer, {'source': 'creator'})
    }

class TagSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Serializes and deserializes a Tag for a Point.
    Validates each deserialized field.
    """

    _url = NestedHyperlinkedIdentityField(
        read_only=True,
        view_name='point-tag-detail',
        parent_lookup_kwargs={'point_pk': 'point__pk'}
    )
    point = wrap_url(serializers.HyperlinkedRelatedField)(read_only=True, view_name='point-detail')
    creator = wrap_url(serializers.HyperlinkedRelatedField)(read_only=True, view_name='user-detail')

    class Meta:
       model = Tag
       fields = ('_url', 'id', 'name', 'created', 'point', 'creator')

    expandable_fields = {
        'creator': (CreatorSerializer, {'source': 'creator'}),
    }

class StarSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Serializes and deserializes a Star for a Point.
    Validates each deserialized field.
    """

    _url = NestedHyperlinkedIdentityField(
        read_only=True,
        view_name='point-star-detail',
        parent_lookup_kwargs={'point_pk': 'point__pk'}
    )
    point = wrap_url(serializers.HyperlinkedRelatedField)(read_only=True, view_name='point-detail')
    creator = wrap_url(serializers.HyperlinkedRelatedField)(read_only=True, view_name='user-detail')

    class Meta:
       model = Star
       fields = ('_url', 'id', 'created', 'point', 'creator')

    expandable_fields = {
        'creator': (CreatorSerializer, {'source': 'creator'}),
    }

class PointSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Serializes and deserializes a Point.
    Validates each deserialized field.
    """

    creator = wrap_url(serializers.HyperlinkedRelatedField)(read_only=True, view_name='user-detail')
    comments = wrap_url(NestedHyperlinkedRelatedField)(
        many=True,
        read_only=True,
        view_name='point-comment-detail',
        parent_lookup_kwargs={'point_pk': 'point__pk'}
    )
    tags = wrap_url(NestedHyperlinkedRelatedField)(
        many=True,
        read_only=True,
        view_name='point-tag-detail',
        parent_lookup_kwargs={'point_pk': 'point__pk'}
    )
    stars = wrap_url(NestedHyperlinkedRelatedField)(
        many=True,
        read_only=True,
        view_name='point-star-detail',
        parent_lookup_kwargs={'point_pk': 'point__pk'}
    )

    class Meta:
        model = Point
        fields = ('_url', 'id', 'name', 'latitude', 'longitude', 'description', 'created', 'creator', 'comments', 'tags', 'stars')

    def to_representation(self, instance):
        """
        Override the default serialization to add '_url' and '_parent' link attributes
        to nested resources (comments, tags and stars).

        Parameters:
            - instance: the Point model instance to serialize.

        Returns:
            - serialized Point data
        """

        data = super().to_representation(instance)
        uri = self.context['request'].build_absolute_uri()
        url = get_url(uri)

        if self.context.get('action') in ['list', 'create', 'delete'] and hasattr(instance, 'pk'):
            url = '{}{}/'.format(url, instance.pk)

        if hasattr(instance, 'pk'):
            parent_url = '{}{}/'.format(get_parent_url(url), instance.pk)
        else:
            parent_url = '{}/'.format(get_parent_url(url))

        data['comments'] = {'_items': data['comments'], '_url': url + 'comments/', '_parent': parent_url}
        data['tags'] = {'_items': data['tags'], '_url': url + 'tags/', '_parent': parent_url}
        data['stars'] = {'_items': data['stars'], '_url': url + 'stars/', '_parent': parent_url}

        return data

    expandable_fields = {
        'creator': (CreatorSerializer, {'source': 'creator'}),
        'comments': (CommentSerializer, {'source': 'comments', 'many': True}),
        'tags': (TagSerializer, {'source': 'tags', 'many': True}),
        'stars': (StarSerializer, {'source': 'stars', 'many': True})
    }

class UserPointSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Serializes and deserializes a Point under a User.
    Validates each deserialized field.
    """

    class Meta:
        model = Point
        fields = ('_url', 'id', 'name', 'latitude', 'longitude', 'description', 'created', 'creator')

class UserSerializer(FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer):
    """
    Serializes and deserializes a User.
    Validates each deserialized field.
    """

    points = wrap_url(serializers.HyperlinkedRelatedField)(many=True, read_only=True, view_name='point-detail')
    comments = wrap_url(NestedHyperlinkedRelatedField)(
        many=True,
        read_only=True,
        view_name='point-comment-detail',
        parent_lookup_kwargs={'point_pk': 'point__pk'}
    )
    stars = wrap_url(NestedHyperlinkedRelatedField)(
        many=True,
        read_only=True,
        view_name='point-star-detail',
        parent_lookup_kwargs={'point_pk': 'point__pk'}
    )

    def update(self, instance, data):
        """
        Override update with set_password to hash the User's password
        when updating a User.

        Adapted from https://stackoverflow.com/a/27586289.

        Parameters:
            - data: the request body data to handle

        Returns:
            - the updated User model instance
        """

        for key, value in data.items():
            if key == 'password':
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()
        return instance

    def create(self, data):
        """
        Override create with set_password to hash the User's password
        when creating a new User.

        Adapted from https://stackoverflow.com/a/27586289.

        Parameters:
            - data: the request body data to handle

        Returns:
            - the created User model instance
        """

        password = data.pop('password', None)
        instance = self.Meta.model(**data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Override the default serialization to add '_url' and '_parent' link attributes
        to nested resources (points, comments and stars).

        Parameters:
            - instance: the User model instance to serialize.

        Returns:
            - serialized User data
        """

        data = super().to_representation(instance)
        uri = self.context['request'].build_absolute_uri()
        url = get_url(uri)

        if self.context.get('action') in ['list', 'create', 'delete'] and hasattr(instance, 'pk'):
            url = '{}{}/'.format(url, instance.pk)

        if hasattr(instance, 'pk'):
            parent_url = '{}{}/'.format(get_parent_url(url), instance.pk)
        else:
            parent_url = '{}/'.format(get_parent_url(url))

        data['points'] = {'_items': data['points'], '_url': url + 'points/', '_parent': parent_url}
        data['comments'] = {'_items': data['comments'], '_url': url + 'comments/', '_parent': parent_url}
        data['stars'] = {'_items': data['stars'], '_url': url + 'stars/', '_parent': parent_url}

        return data

    class Meta:
        model = User
        fields = ('_url', 'id', 'username', 'password', 'location', 'points', 'comments', 'stars', 'created')
        extra_kwargs = {'password': {'write_only': True}}

    expandable_fields = {
        'points': (PointSerializer, {'source': 'points', 'many': True}),
        'comments': (CommentSerializer, {'source': 'comments', 'many': True}),
        'stars': (StarSerializer, {'source': 'stars', 'many': True})
    }
