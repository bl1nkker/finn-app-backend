from django.contrib import admin
from .models import Facility, Revenue, Employee
from .models import Importer, ProductionType, Role, UserFacility

admin.site.register(Facility)
admin.site.register(Revenue)
admin.site.register(Employee)
admin.site.register(Importer)
admin.site.register(ProductionType)
admin.site.register(Role)
admin.site.register(UserFacility)
