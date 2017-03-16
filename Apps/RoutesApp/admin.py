from django.contrib import admin

from Apps.RoutesApp.models import Route
from Apps.RoutesApp.models import User
from Apps.RoutesApp.models import Rating

# Register your models here.

admin.site.register(Route)
admin.site.register(User)
admin.site.register(Rating)