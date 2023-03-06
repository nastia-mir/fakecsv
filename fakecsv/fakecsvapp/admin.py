from django.contrib import admin

from fakecsvapp import models

admin.site.register(models.FullNameColumn)
admin.site.register(models.EmailColumn)
admin.site.register(models.DomainNameColumn)
admin.site.register(models.PhoneNumberColumn)
admin.site.register(models.DateColumn)
admin.site.register(models.Schema)
admin.site.register(models.SchemaColumn)

