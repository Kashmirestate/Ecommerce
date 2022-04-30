from gettext import Catalog
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)

admin.site.register(catagory)
admin.site.register(SubCatagory)
admin.site.register(cover)
admin.site.register(filedata)
