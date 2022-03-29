from django.contrib import admin

from app.models import Workflow, Owner, Inventor, TechnologyType, \
    Status, Asset


admin.site.register(Workflow)
admin.site.register(Owner)
admin.site.register(Inventor)
admin.site.register(TechnologyType)
admin.site.register(Status)
admin.site.register(Asset)
