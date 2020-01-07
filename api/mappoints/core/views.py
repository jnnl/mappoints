from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from mappoints.core.models import User, Point, Comment, Star, Tag
from mappoints.core.serializers import (UserSerializer,
                                        PointSerializer,
                                        CommentSerializer,
                                        TagSerializer,
                                        StarSerializer)
from mappoints.core.permissions import (IsCreator,
                                        IsSelf,
                                        ActionPermission)
from mappoints.core.responses import LinkedCollectionResponse, LinkedInstanceResponse


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Handle create, read, update and delete actions for a User resource.

    URLs: /users/, /users/:user_id
    """

    serializer_class = UserSerializer
    queryset = User.objects.filter()

    permission_classes = (ActionPermission,)
    action_permissions = {
        permissions.AllowAny: ['list', 'retrieve', 'create'],
        IsSelf: ['update', 'destroy'],
    }

    def list(self, request):
        """
        Get all users.

        Returns:
            - list of all users.
        """

        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True, context={'request': request, 'action': 'list'})
        return LinkedCollectionResponse(serializer.data, request)

    def retrieve(self, request, pk=None):
        """
        Get a single user.

        Path parameters:
            - pk: id of the user.

        Returns:
            - single user object.
        """

        queryset = User.objects.filter()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, context={'request': request, 'action': 'retrieve'})
        return LinkedInstanceResponse(serializer.data, request)

    def update(self, request, *args, **kwargs):
        """
        Update a single user's details.

        Returns:
            - updated user object.
        """

        response = super().update(request, *args, **kwargs)
        return LinkedInstanceResponse(response.data, request, status=200)

    def create(self, request, *args, **kwargs):
        """
        Create a new user.

        Errors:
            - a user with the same username already exists (409)

        Returns:
            - created user object.
        """

        try:
            user = User.objects.get(username=request.data.get('username'))
            if user:
                return Response({'detail': 'A user with this username already exists.'}, status=409)
        except User.DoesNotExist:
            pass

        response = super().create(request, *args, **kwargs)
        return LinkedInstanceResponse(response.data, request, status=201)

class UserPointViewSet(viewsets.ViewSet):
    """
    Handle read actions for a Point resource under a User.

    URLs: /users/:user_id/points/, /users/:user_id/points/:point_id
    """

    serializer_class = PointSerializer

    def initial(self, request, *args, **kwargs):
        """
        Ensure that the specified user exists before handling any actions.

        Path parameters:
            - user_pk: id of the user whose points are of interest.
        """

        get_object_or_404(User.objects.all(), pk=kwargs['user_pk'])
        return super().initial(request, args, kwargs)

    def list(self, request, user_pk=None):
        """
        Get all points of a specified user.

        Path parameters:
            - user_pk: id of the user whose points are retrieved.

        Returns:
            - list of all points of a user.
        """

        queryset = Point.objects.filter(creator=user_pk)
        serializer = PointSerializer(queryset, many=True, context={'request': request, 'action': 'list'})
        return LinkedCollectionResponse(serializer.data, request)

    def retrieve(self, request, pk=None, user_pk=None):
        """
        Get a single point of a specified user.

        Path parameters:
            - user_pk: id of the user whose point is retrieved.
            - pk: id of the point to retrieve.

        Returns:
            - single point object of the specified user.
        """

        queryset = Point.objects.filter(pk=pk, creator=user_pk)
        point = get_object_or_404(queryset, pk=pk)
        serializer = PointSerializer(point, context={'request': request, 'action': 'retrieve'})
        return LinkedInstanceResponse(serializer.data, request)

class UserCommentViewSet(viewsets.ViewSet):
    """
    Handle read actions for a Comment resource under a User.

    URLs: /users/:user_id/comments/, /users/:user_id/comments/:comment_id
    """

    serializer_class = CommentSerializer

    def initial(self, request, *args, **kwargs):
        """
        Ensure that the specified user exists before handling any actions.

        Path parameters:
            - user_pk: id of the user whose comments are of interest.
        """

        get_object_or_404(User.objects.all(), pk=kwargs['user_pk'])
        return super().initial(request, args, kwargs)

    def list(self, request, user_pk=None):
        """
        Get all comments of a specified user.

        Path parameters:
            - user_pk: id of the user whose comments are retrieved.

        Returns:
            - list of all comments of a user.
        """

        queryset = Comment.objects.filter(creator=user_pk)
        serializer = CommentSerializer(queryset, many=True, context={'request': request, 'action': 'list'})
        return LinkedCollectionResponse(serializer.data, request)

    def retrieve(self, request, pk=None, user_pk=None):
        """
        Get a single comment of a specified user.

        Path parameters:
            - user_pk: id of the user whose comment is retrieved.
            - pk: id of the comment to retrieve.

        Returns:
            - single comment object of the specified user.
        """

        queryset = Comment.objects.filter(pk=pk, creator=user_pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment, context={'request': request, 'action': 'retrieve'})
        return LinkedInstanceResponse(serializer.data, request)

class UserStarViewSet(viewsets.ViewSet):
    """
    Handle read actions for a Star resource under a User.

    URLs: /users/:user_id/stars/, /users/:user_id/stars/:star_id
    """

    serializer_class = StarSerializer

    def initial(self, request, *args, **kwargs):
        """
        Ensure that the specified user exists before handling any actions.

        Path parameters:
            - user_pk: id of the user whose stars are of interest.
        """

        get_object_or_404(User.objects.all(), pk=kwargs['user_pk'])
        return super().initial(request, args, kwargs)

    def list(self, request, user_pk=None):
        """
        Get all stars of a specified user.

        Path parameters:
            - user_pk: id of the user whose stars are retrieved.

        Returns:
            - list of all stars of a user.
        """

        queryset = Star.objects.filter(creator=user_pk)
        serializer = StarSerializer(queryset, many=True, context={'request': request, 'action': 'list'})
        return LinkedCollectionResponse(serializer.data, request)

    def retrieve(self, request, pk=None, user_pk=None):
        """
        Get a single star of a specified user.

        Path parameters:
            - user_pk: id of the user whose star is retrieved.
            - pk: id of the star to retrieve.

        Returns:
            - single star object of the specified user.
        """
        queryset = Star.objects.filter(pk=pk, creator=user_pk)
        star = get_object_or_404(queryset, pk=pk)
        serializer = StarSerializer(star, context={'request': request, 'action': 'retrieve'})
        return LinkedInstanceResponse(serializer.data, request)

class PointViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    Handle create, read, update and delete actions for a Point.

    URLs: /points/, /points/:point_id/
    """

    serializer_class = PointSerializer
    queryset = Point.objects.filter()

    permission_classes = (ActionPermission,)
    action_permissions = {
        permissions.AllowAny: ['list', 'retrieve'],
        permissions.IsAuthenticated: ['create'],
        IsCreator: ['update', 'destroy'],
    }

    def list(self, request):
        """
        Get all points.

        Returns:
            - list of all points.
        """

        queryset = Point.objects.filter()
        serializer = PointSerializer(queryset, many=True, context={'request': request, 'action': 'list'})
        return LinkedCollectionResponse(serializer.data, request)

    def retrieve(self, request, pk=None):
        """
        Get a single point.

        Path parameters:
            - pk: id of the point to retrieve.

        Returns:
            - single point object.
        """

        queryset = Point.objects.filter(pk=pk)
        point = get_object_or_404(queryset, pk=pk)
        serializer = PointSerializer(point, context={'request': request, 'action': 'retrieve'})
        return LinkedInstanceResponse(serializer.data, request)

    def update(self, request, *args, **kwargs):
        """
        Update a single point's details.

        Returns:
            - updated point object.
        """

        response = super().update(request, *args, **kwargs)
        return LinkedInstanceResponse(response.data, request)

    def create(self, request, *args, **kwargs):
        """
        Create a new point.

        Errors:
            - a point with the same name by the user already exists (409)

        Returns:
            - created point object.
        """

        try:
            point = Point.objects.get(name=request.data.get('name'), creator=request.user.id)
            if point:
                return Response({'detail': 'A point with this name by this user already exists.'}, status=409)
        except Point.DoesNotExist:
            pass

        response = super().create(request, *args, **kwargs)
        return LinkedInstanceResponse(response.data, request, status=201)

    def perform_create(self, serializer):
        """
        Set the current user as the creator of the point.
        """

        serializer.save(creator=self.request.user)

class PointCommentViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """
    Handle create, read, update and delete actions for a Comment resource under a point.

    URLs: /points/:point_id/comments/, /points/:point_id/comments/:comment_id/
    """


    serializer_class = CommentSerializer
    queryset = Comment.objects.filter()

    permission_classes = (ActionPermission,)
    action_permissions = {
        permissions.AllowAny: ['list', 'retrieve'],
        permissions.IsAuthenticated: ['create'],
        IsCreator: ['update', 'destroy'],
    }

    def initial(self, request, *args, **kwargs):
        """
        Ensure that the specified point exists before handling any actions.

        Path parameters:
            - point_pk: id of the point whose comments are of interest.
        """

        get_object_or_404(Point.objects.all(), pk=kwargs['point_pk'])
        return super().initial(request, args, kwargs)

    def list(self, request, point_pk=None):
        """
        Get all comments for a specified point.

        Path parameters:
            - user_pk: id of the point whose comments are retrieved.

        Returns:
            - list of all comments for a point.
        """

        queryset = Comment.objects.filter(point=point_pk)
        serializer = CommentSerializer(queryset, many=True, context={'request': request, 'action': 'list'})
        return LinkedCollectionResponse(serializer.data, request)

    def retrieve(self, request, pk=None, point_pk=None):
        """
        Get a single comment for a point.

        Path parameters:
            - point_pk: id of the point the comment is for.
            - pk: id of the comment to retrieve.

        Returns:
            - single comment object.
        """

        queryset = Comment.objects.filter(pk=pk, point=point_pk)
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment, context={'request': request, 'action': 'retrieve'})
        return LinkedInstanceResponse(serializer.data, request)

    def update(self, request, *args, **kwargs):
        """
        Update a single comments's details for a point.

        Returns:
            - updated comment object.
        """

        response = super().update(request, *args, **kwargs)
        return LinkedInstanceResponse(response.data, request)

    def create(self, request, *args, **kwargs):
        """
        Create a new comment for a point.

        Path parameters:
            - point_pk: id of the point the comment is for.

        Returns:
            - created comment object.
        """

        response = super().create(request, *args, **kwargs)
        return LinkedInstanceResponse(response.data, request, status=201)

    def perform_create(self, serializer):
        """
        Set the current user as the creator of the comment and the point as the target point.

        Path parameters:
            - point_pk: id of the point the comment is for.
        """

        serializer.save(creator=self.request.user, point_id=self.kwargs['point_pk'])

class PointTagViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    Handle create, read, update and delete actions for a Tag resource under a point.

    URLs: /points/:point_id/tags/, /points/:point_id/tags/:tag_id/
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.filter()

    permission_classes = (ActionPermission,)
    action_permissions = {
        permissions.AllowAny: ['list', 'retrieve'],
        IsCreator: ['create', 'update', 'destroy'],
    }

    def initial(self, request, *args, **kwargs):
        """
        Ensure that the specified point exists before handling any actions.

        Path parameters:
            - point_pk: id of the point whose tags are of interest.
        """

        get_object_or_404(Point.objects.all(), pk=kwargs['point_pk'])
        return super().initial(request, args, kwargs)

    def list(self, request, point_pk=None):
        """
        Get all tags for a specified point.

        Path parameters:
            - user_pk: id of the point whose tags are retrieved.

        Returns:
            - list of all tags for a point.
        """

        queryset = Tag.objects.filter(point=point_pk)
        serializer = TagSerializer(queryset, many=True, context={'request': request, 'action': 'list'})
        return LinkedCollectionResponse(serializer.data, request)

    def retrieve(self, request, pk=None, point_pk=None):
        """
        Get a single tag for a point.

        Path parameters:
            - point_pk: id of the point the tag is for.
            - pk: id of the tag to retrieve.

        Returns:
            - single tag object.
        """

        queryset = Tag.objects.filter(pk=pk, point=point_pk)
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TagSerializer(tag, context={'request': request, 'action': 'retrieve'})
        return LinkedInstanceResponse(serializer.data, request)

    def update(self, request, *args, **kwargs):
        """
        Update a single tags's details for a point.

        Returns:
            - updated tag object.
        """

        response = super().update(request, *args, **kwargs)
        return LinkedInstanceResponse(response.data, request)

    def create(self, request, *args, **kwargs):
        """
        Create a new tag for a point.

        Path parameters:
            - point_pk: id of the point the tag is for.

        Errors:
            - the creator of the tag is not the creator of the point (403)

        Returns:
            - created tag object.
        """

        point = get_object_or_404(Point.objects.filter(id=self.kwargs['point_pk']))
        if point.creator.id != request.user.id:
            return Response({'detail': 'Only the creator of the point can create tags for it.'}, status=403)

        response = super().create(request, *args, **kwargs)
        return LinkedInstanceResponse(response.data, request, status=201)

    def perform_create(self, serializer):
        """
        Set the current user as the creator of the tag and the point as the target point.

        Path parameters:
            - point_pk: id of the point the tag is for.
        """

        serializer.save(creator=self.request.user, point_id=self.kwargs['point_pk'])

class PointStarViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """
    Handle create, read and delete actions for a Star resource under a point.

    URLs: /points/:point_id/stars/, /points/:point_id/stars/:star_id/
    """

    serializer_class = StarSerializer
    queryset = Star.objects.filter()

    permission_classes = (ActionPermission,)
    action_permissions = {
        permissions.AllowAny: ['list', 'retrieve'],
        permissions.IsAuthenticated: ['create'],
        IsCreator: ['destroy'],
    }

    def initial(self, request, *args, **kwargs):
        """
        Ensure that the specified point exists before handling any actions.

        Path parameters:
            - point_pk: id of the point whose stars are of interest.
        """

        get_object_or_404(Point.objects.all(), pk=kwargs['point_pk'])
        return super().initial(request, args, kwargs)

    def list(self, request, point_pk=None):
        """
        Get all stars for a specified point.

        Path parameters:
            - user_pk: id of the point whose stars are retrieved.

        Returns:
            - list of all stars for a point.
        """

        queryset = Star.objects.filter(point=point_pk)
        serializer = StarSerializer(queryset, many=True, context={'request': request, 'action': 'list'})
        return LinkedCollectionResponse(serializer.data, request)

    def retrieve(self, request, pk=None, point_pk=None):
        """
        Get a single star for a point.

        Path parameters:
            - point_pk: id of the point the star is for.
            - pk: id of the star to retrieve.

        Returns:
            - single star object.
        """

        queryset = Star.objects.filter(pk=pk, point=point_pk)
        star = get_object_or_404(queryset, pk=pk)
        serializer = StarSerializer(star, context={'request': request, 'action': 'retrieve'})
        return LinkedInstanceResponse(serializer.data, request)

    def create(self, request, *args, **kwargs):
        """
        Create a new star for a point.

        Path parameters:
            - point_pk: id of the point the star is for.

        Errors:
            - a star by the user already exists (409)

        Returns:
            - created star object.
        """

        try:
            star = Star.objects.get(point=self.kwargs['point_pk'], creator=request.user.id)
            if star:
                return Response({'detail': 'A star for this point by this user already exists.'}, status=409)
        except Star.DoesNotExist:
            pass

        response = super().create(request, *args, **kwargs)
        return LinkedInstanceResponse(response.data, request, status=201)

    def perform_create(self, serializer):
        """
        Set the current user as the creator of the star and the point as the target point.

        Path parameters:
            - point_pk: id of the point the star is for.
        """

        serializer.save(creator=self.request.user, point_id=self.kwargs['point_pk'])
