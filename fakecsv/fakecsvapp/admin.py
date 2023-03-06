from django.contrib import admin

from fakecsvapp import models

admin.site.register(models.Schema)
admin.site.register(models.SchemaColumn)
admin.site.register(models.DataSets)

