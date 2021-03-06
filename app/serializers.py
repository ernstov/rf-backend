import pandas as pd
import numpy as np

from django.utils.translation import gettext as _
from django.db import transaction
from django.forms.models import model_to_dict

from rest_framework import serializers, exceptions

from app import models


class WorkflowSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Workflow
        fields = ("id", "name", "description", "type")


class AssetSerializer(serializers.ModelSerializer):

    def to_representation(self, data):
        data = super().to_representation(data)
        owners = []
        inventors = []
        techbologies = []
        workflows = []
        if data.get("owners", None):
            for owner in data["owners"]:
                owner_obj = model_to_dict(models.Owner.objects.get(id=owner))
                owners.append(owner_obj)

        if data.get("inventors", None):
            for inventor in data["inventors"]:
                inventor_obj = model_to_dict(models.Inventor.objects.get(id=inventor))
                inventors.append(inventor_obj)

        if data.get("workflow", None):
            for workflow in data["workflow"]:
                workflow_obj = model_to_dict(models.Workflow.objects.get(id=workflow))
                workflows.append(workflow_obj)

        if data.get("technology_types", None):
            for technology in data["technology_types"]:
                techbology_obj = model_to_dict(models.TechnologyType.objects.get(id=technology))
                techbologies.append(techbology_obj)

        status = models.Status.objects.get(id=data["status"])

        asset_data = {
            "uuid": data["uuid"],
            "title": data["title"],
            "owners": owners,
            "inventors": inventors,
            "patent_numbers": data.get("patent_numbers", []),
            "family_id": data.get("family_id", ""),
            "publication_date": data.get("publication_date", ""),
            "priority_date": data.get("priority_date", ""),
            "expiry_date": data.get("expiry_date", ""),
            "technology_types": techbologies,
            "status": {
                "id": status.id,
                "name": status.name
            },
            "workflow": workflows,
            "abstract": data.get("abstract", ""),
            "description": data.get("description", ""),
            "claims": data.get("claims", ""),
        }
        return asset_data



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

    def to_representation(self, data):
        data = super().to_representation(data)
        techbologies = []
        workflows = []

        if data.get("workflow", None):
            for workflow in data["workflow"]:
                workflow_obj = model_to_dict(models.Workflow.objects.get(id=workflow))
                workflows.append(workflow_obj)

        if data.get("technology_types", None):
            for technology in data["technology_types"]:
                techbology_obj = model_to_dict(models.TechnologyType.objects.get(id=technology))
                techbologies.append(techbology_obj)

        status = models.Status.objects.get(id=data["status"])

        return {
            "status": {
                "id": status.id,
                "name": status.name
            },
            "techbology_types": techbologies,
            "workflow": workflows
        }

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


class BulkuploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    workflows = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    class Meta:
        fields = ("file", "workflows")

    def validate(self, attrs):
        file_ext = attrs["file"].name.split(".")[-1]
        if file_ext != "csv":
            raise exceptions.UnsupportedMediaType(file_ext)
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        file = validated_data["file"]
        reader = pd.read_csv(file)
        workflows = ''
        if validated_data.get("workflows", None):
            workflows = [models.Workflow.objects.get(id=workflow_id) for workflow_id in validated_data["workflows"]]
        for i, row in reader.iterrows():
            row_dict = row.to_dict()
            owners = [
                models.Owner.objects.get_or_create(name=owner.strip())[0] for owner in row_dict["Owners"].split("|")
            ]
            inventors = [
                models.Inventor.objects.get_or_create(name=inventor.strip())[0] for inventor in row_dict["Inventors"].split("|")
            ]
            technologies = [
                models.TechnologyType.objects.get_or_create(name=technology.strip())[0] for technology in row_dict["Technology"].split("|")
            ]

            pending_territories = []
            if row_dict["Pending Territories"] is not np.nan:
                for country in row_dict["Pending Territories"].split("|"):
                    try:
                        pending_territories.append(
                            models.Country.objects.get(code=country.strip()[:2])
                        )
                    except models.Country.DoesNotExist:
                        raise exceptions.NotFound(
                            _(f"'{country.strip()[:2]}' country not found in database")
                        )

            granted_territories = []
            if row_dict["Granted Territories"] is not np.nan:
                for country in row_dict["Granted Territories"].split("|"):
                    try:
                        granted_territories.append(
                            models.Country.objects.get(code=country.strip()[:2])
                        )
                    except models.Country.DoesNotExist:
                        raise exceptions.NotFound(
                            _(f"'{country.strip()[:2]}' country not found in database")
                        )

            expired_territories = []
            if row_dict["Expired Territories"] is not np.nan:
                for country in row_dict["Expired Territories"].split("|"):
                    try:
                        expired_territories.append(
                            models.Country.objects.get(code=country.strip()[:2])
                        )
                    except models.Country.DoesNotExist:
                        raise exceptions.NotFound(
                            _(f"'{country.strip()[:2]}' country not found in database")
                        )
            try:
                if models.Asset.objects.filter(family_id=row_dict["Cipher Family ID"]):
                    raise Exception("Asset already exists")

                asset = models.Asset.objects.create(
                    family_id=row_dict["Cipher Family ID"],
                    title=row_dict["Title"],
                    publication_date=row_dict.get("Publication Date", ""),
                    priority_date=row_dict.get("Priority Date", ""),
                    expiry_date=row_dict.get("Expiry Date", ""),
                    patent_numbers=[x.strip() for x in row_dict["Patent Numbers"].split(" ")],
                    status=models.Status.objects.get_or_create(name=row_dict["Status"])[0],
                    cipher_score=row_dict["Score"] if row_dict["Score"] else 0,
                    pvix_score=row_dict["Pvix Score"] if row_dict["Pvix Score"] else 0,
                    backward_citations=row_dict["Backward citations"] if row_dict["Backward citations"] else 0,
                    forward_citations=row_dict["Forward citations"] if row_dict["Forward citations"] else 0,
                    future_cost_projection=row_dict["Future Cost Projection [USD]"] if row_dict["Future Cost Projection [USD]"] else 0,
                    cost_to_date=row_dict["Cost to date [USD]"] if row_dict["Cost to date [USD]"] else 0,
                    added_by=self.context["request"].user
                )
            except Exception:
                pass

            if row_dict["Granted Date"] is not np.nan:
                asset.granted_date = row_dict["Granted Date"]
                asset.save()

            if owners:
                asset.owners.add(*owners)

            if inventors:
                asset.inventors.add(*inventors)

            if workflows:
                asset.workflow.add(*workflows)

            if technologies:
                asset.technology_types.add(*technologies)

            if pending_territories:
                asset.pending_territories.add(*pending_territories)

            if granted_territories:
                asset.granted_territories.add(*granted_territories)

            if expired_territories:
                asset.expired_territories.add(*expired_territories)
        return {}
