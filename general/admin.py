from django.contrib import admin
from general.models import Airport, priceType, priceTemplate, Price


# Register your models here.
admin.site.register(Airport)
admin.site.register(priceType)
admin.site.register(priceTemplate)
admin.site.register(Price)