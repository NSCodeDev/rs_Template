from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExampleModelViewSet

router = DefaultRouter()
"""
1. Register the ExampleModelViewSet with the router
2. Give it the prefix 'example', let's say for user you can give 'users', for products 'products' etc.

"""
router.register(r"example", ExampleModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
