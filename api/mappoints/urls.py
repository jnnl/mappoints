"""
mappoints URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_nested import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from mappoints.core import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='user')
router.register(r'points', views.PointViewSet, base_name='point')

users_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
users_router.register(r'points', views.UserPointViewSet, base_name='user-point')
users_router.register(r'comments', views.UserCommentViewSet, base_name='user-comment')
users_router.register(r'stars', views.UserStarViewSet, base_name='user-star')

points_router = routers.NestedDefaultRouter(router, r'points', lookup='point')
points_router.register(r'comments', views.PointCommentViewSet, base_name='point-comment')
points_router.register(r'stars', views.PointStarViewSet, base_name='point-star')
points_router.register(r'tags', views.PointTagViewSet, base_name='point-tag')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(users_router.urls)),
    url(r'^', include(points_router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]
