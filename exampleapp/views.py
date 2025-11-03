from rest_framework.viewsets import ModelViewSet

from .models import ExampleModel
from .serializers import ExampleModelSerializer

# Create your views here.


class ExampleModelViewSet(ModelViewSet):
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer
