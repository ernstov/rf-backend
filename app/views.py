from django.http import Http404
from rest_framework import viewsets, permissions, status, mixins, filters, generics
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from app import models
from app import serializers
from app.pagination import CustomPageNumberPagination


class WorkflowViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.WorkflowSerializer
    queryset = models.Workflow.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]
    filterset_fields = ["type"]


class AssetsViewset(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        """
        Returns AssetSerializer on post request
        and AssetEditSerializer on put or patch request
        """
        if self.request.method == "POST" or self.request.method == "GET":
            return serializers.AssetSerializer
        return serializers.AssetEditSerializer

    def retrieve(self, request, *args, **kwargs):
        asset = models.Asset.objects.get(uuid=self.kwargs["pk"])
        serializer = self.get_serializer(asset)

        return Response(serializer.data)

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
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class BulkUploadViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BulkuploadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({}, status=status.HTTP_201_CREATED)
