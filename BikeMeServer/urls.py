"""RestAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Apps.BikeMe.views import  recommender_system_view, user_view, route_view, event_view, problem_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^recommendersystem$', recommender_system_view.getAllData),

    url(r'^users/new$', user_view.createUser),
    url(r'^users/workouts/new$', user_view.createWorkouts),
    url(r'^users/(?P<pk>[\w\-]+)/update$', user_view.updateUser),

    url(r'^routes/new$', route_view.createRoute),
    url(r'^routes/valid$', route_view.isRouteValid),
    url(r'^routes/ratings/new$', route_view.createRatings),

    url(r'^events/guests/new$', event_view.createGuests),

    url(r'^problems/new$', problem_view.createProblems),
]
