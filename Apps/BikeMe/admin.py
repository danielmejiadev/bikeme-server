from django.contrib import admin

from Apps.BikeMe.models.route_model import Route
from Apps.BikeMe.models.user_model import User
from Apps.BikeMe.models.workout_model import Workout
from Apps.BikeMe.models.rating_model import Rating
from Apps.BikeMe.models.point_model import Point
from Apps.BikeMe.models.event_model import Event
from Apps.BikeMe.models.guest_model import Guest
from Apps.BikeMe.models.challenge_model import Challenge

# Register your models here.

admin.site.register(User)
admin.site.register(Workout)
admin.site.register(Route)
admin.site.register(Rating)
admin.site.register(Point)
admin.site.register(Event)
admin.site.register(Guest)
admin.site.register(Challenge)