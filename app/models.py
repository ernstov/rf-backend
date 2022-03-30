from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import ArrayField

from core.mixins import UUIDBaseMixin


class Workflow(models.Model):
    class TypeChoices(models.TextChoices):
        PROJECT = ("project", _("Project"))
        PROGRAM = ("program", _("Program"))
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    type = models.CharField(choices=TypeChoices.choices, max_length=50)
    archived = models.BooleanField(default=False)


class Shortlist(models.Model):
    class StatusChoice(models.TextChoices):
        NEW = ("new", _("New"))
        UNDER_TECH_EVAL = ("ute", _("Under Technical Evaluation"))
        UNDER_COMM_EVAL = ("uce", _("Under Commercial Evaluation"))
        REJECTED = ("rejected", _("Rejected"))
        ORPHAN = ("orphan", _("Orphan"))
        UNDER_NEGOTIATION = ("under negotiation", _("Under Negotiation"))
        ACQUIRED = ("acquired", _("Acquired"))
        UNAVAILABLE = ("unavailable", _("Unavailable"))

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    archived = models.BooleanField(default=False)
    status = models.CharField(choices=StatusChoice.choices, max_length=50)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)


class TechnologyType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    archived = models.BooleanField(default=False)


class Inventor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    archived = models.BooleanField(default=False)


class CPCCode(models.Model):
    code = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    archived = models.BooleanField(default=False)


class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"


class Source(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    archived = models.BooleanField(default=False)


class Owner(models.Model):
    class OwnerTypeChoices(models.TextChoices):
        LARGE_FMCG = ("fmcg", _("Large FMCG"))
        PACKAGING_COMPITITOR = (
            "packaging compititor",
            _("Packaging Compititor")
        )
        SME = ("sme", _("SME (Small/Medium) Enterprise"))
        PRIVATE_INDIVIDUAL = ("pvt individual", _("Private Individual"))
        UNIVERSITY_TTO = ("univeristy", _("University / TTO"))
        OTHER = ("other", _("Other"))

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    archived = models.BooleanField(default=False)
    owner_type = models.CharField(
        choices=OwnerTypeChoices.choices,
        max_length=50
    )


class Assignee(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    archived = models.BooleanField(default=False)
    assignee_type = models.CharField(
        choices=Owner.OwnerTypeChoices.choices,
        max_length=50
    )


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True)


class Asset(UUIDBaseMixin):
    family_id = models.CharField(unique=True, max_length=255)
    patent_numbers = ArrayField(
        models.CharField(max_length=50),
        unique=True,
        null=True,
        blank=True
    )
    inventors = models.ManyToManyField(Inventor, blank=True)
    description = models.TextField()
    abstract = models.TextField()
    claims = models.TextField()
    title = models.CharField(max_length=255)
    priority_date = models.DateField()
    publication_date = models.DateField()
    expiry_date = models.DateField()
    cost_to_date = models.FloatField(null=True, blank=True)
    future_cost_projection = models.FloatField(null=True, blank=True)
    cipher_score = models.FloatField(null=True, blank=True)
    pvix_score = models.FloatField(null=True, blank=True)
    organisation = ArrayField(
        models.CharField(unique=True, max_length=255),
        null=True,
        blank=True
    )
    backward_citations = models.IntegerField(null=True, blank=True)
    forward_citations = models.IntegerField(null=True, blank=True)
    prepatent = models.BooleanField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    assigness = ArrayField(
        models.CharField(max_length=255),
        null=True,
        blank=True
    )
    owners = models.ManyToManyField(Owner)
    technology_types = models.ManyToManyField(TechnologyType)
    workflow = models.ManyToManyField(Workflow)
    pending_territories = models.ManyToManyField(
        Country,
        related_name="pending_territories",
        blank=True
    )
    granted_territories = models.ManyToManyField(
        Country,
        related_name="granted_territories",
        blank=True
    )
    expired_territories = models.ManyToManyField(
        Country,
        related_name="expired_territories",
        blank=True
    )
    cpc_code = models.ManyToManyField(CPCCode, blank=True)
