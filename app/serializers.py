from django.utils.translation import gettext as _

from rest_framework import serializers, exceptions

from app import models


class WorkflowSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Workflow
        fields = ("id", "name", "description", "type")


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Asset
        fields = (
            "uuid",
            "title",
            "owners",
            "inventors",
            "patent_numbers",
            "family_id",
            "publication_date",
            "priority_date",
            "expiry_date",
            "technology_types",
            "status",
            "workflow",
            "abstract",
            "description",
            "claims"
        )

    def create(self, validated_data):
        owners = validated_data.pop("owners", None)
        inventors = validated_data.pop("inventors", None)
        techologies = validated_data.pop("technology_types", None)
        workflow = validated_data.pop("workflow", None)

        asset = models.Asset.objects.create(
            added_by=self.context["request"].user,
            **validated_data
        )

        if workflow:
            asset.workflow.add(*workflow)

        if owners:
            asset.owners.add(*owners)

        if inventors:
            asset.inventors.add(*inventors)

        if techologies:
            asset.technology_types.add(*techologies)

        return asset


class AssetEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Asset
        fields = ("uuid", "technology_types", "status", "workflow")


class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Owner
        fields = ("id", "name", "description", "owner_type", "archived")


class InventorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Inventor
        fields = ("id", "name", "description", "archived")


class TechbologySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TechnologyType
        fields = ("id", "name", "description", "archived")


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Status
        fields = ("id", "name", "description", "archived")
