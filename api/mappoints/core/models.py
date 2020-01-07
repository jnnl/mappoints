from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    """
    The base model that is derived by all the implemented models.
    Adds an automatic created field which denotes when an instance of the model was created.
    """

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class User(BaseModel, AbstractUser):
    """
    The User model. Represents a user that can create and manipulate
    Points, Comments, Tags and Stars.
    Derived from AbstractUser to allow working with Django's built-in authentication.
    """

    location = models.CharField(max_length=100, blank=True, default='')

class Point(BaseModel):
    """
    The Point model. Represents a geographic location.
    """

    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    validators=[MinValueValidator(-180), MaxValueValidator(180)])
    description = models.TextField(blank=True, default='')
    creator = models.ForeignKey(User, related_name='points', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'creator')

class Tag(BaseModel):
    """
    The Tag model. Represents a textual description of the context of a Point (e.g. camping).
    """

    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, related_name='tags', on_delete=models.CASCADE)
    point = models.ForeignKey(Point, related_name='tags', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'point')

class Comment(BaseModel):
    """
    The Comment model. Represents textual content attached by Users to a Point.
    """

    content = models.TextField(default='')
    point = models.ForeignKey(Point, related_name='comments', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

class Star(BaseModel):
    """
    The Star model. Represents a 'like'-esque relation between a User and a Point that is
    established by a User.
    """

    point = models.ForeignKey(Point, related_name='stars', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='stars', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('creator', 'point')
