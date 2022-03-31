from rest_framework import viewsets, permissions, status, mixins, filters
from rest_framework.response import Response

from app import models
from app import serializers


class WorkflowViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.WorkflowSerializer
    queryset = models.Workflow.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class AssetsViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """
        Returns AssetSerializer on post request
        and AssetEditSerializer on put or patch request
        """
        if self.request.method == "POST" or self.request.method == "GET":
            return serializers.AssetSerializer
        return serializers.AssetEditSerializer

    def get_queryset(self):
        return models.Asset.objects.filter(added_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer=serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OwnerViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.OwnerSerializer
    queryset = models.Owner.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class InventorViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.InventorSerializer
    queryset = models.Inventor.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class TechnologyViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TechbologySerializer
    queryset = models.TechnologyType.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class StatusViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.StatusSerializer
    queryset = models.Status.objects.all()
