from django.contrib import admin

from app.models import Workflow, Owner, Inventor, TechnologyType, \
    Status, Asset, Country


admin.site.register(Workflow)
admin.site.register(Owner)
admin.site.register(Inventor)
admin.site.register(TechnologyType)
admin.site.register(Status)
admin.site.register(Asset)
admin.site.register(Country)
