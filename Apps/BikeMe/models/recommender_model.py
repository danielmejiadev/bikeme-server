from Apps.BikeMe.models.route_model import *
from Apps.BikeMe.models.user_model import *
from Apps.BikeMe.models.rating_model import *
import numpy
import copy
import math
from Apps.BikeMe.bikemeutils import BikeMeUtils

class WeigthedSlopeOne():
    def __init__(self):

        self._users = {}
        self._routes = []
   
        for user in User.objects.all():
            ratingsUser ={}
            for rating in user.ratings.filter(calification__gt=0, recommendation=0):
                ratingsUser[str(rating.route.uid)]=rating.calification
        
            self._users[str(user.uid)]=ratingsUser

        for route in Route.objects.all():
            self._routes.append(str(route.uid))

    def _averageDeviations(self):
        self._deviations = {}
        
        num = len(self._routes)
        for i in range(num):
            for j in range(i + 1, num):
                item1 = self._routes[i]
                item2 = self._routes[j]

                r = 0.0
                n = 0
                for key in self._users.keys():
                    user = self._users[key]
                    if item1 in user and item2 in user:
                        r += user[item2] - user[item1]
                        n += 1

                if n > 0:
                    r /= float(n)

                self._deviations[(item1, item2)] = (r, n)
                self._deviations[(item2, item1)] = (-r, n)

    
    def _predict(self, userRatings, item):
        if item in userRatings:
            return userRatings[item]

        if len(userRatings) == 0:
            return 0

        r1 = 0.0
        r2 = 0.0
        for key in userRatings.keys():
            dev, n = self._deviations[(key, item)]
            r1 += (dev + userRatings[key]) * n
            r2 += n

        try:
            return r1 / r2
        except:
            return 0

    def recommends(self, userRatings):
        self._averageDeviations()

        routesNotRated = [route for route in self._routes if route not in userRatings]

        result = []
        for routeNotRated in routesNotRated:
            suggest = self._predict(userRatings,routeNotRated)
            result.append((routeNotRated, suggest))

        return result

    def execute(self):
        saves = []
        for userKey in self._users.keys():
            suggests = self.recommends(self._users[userKey])
            user = User.objects.get(uid=userKey)
            for suggest in suggests:
                recommendation = suggest[1]
                if(recommendation > 0):
                    route = Route.objects.get(uid=suggest[0])
                    try:
                        rating = Rating.objects.get(user=user, route=route, calification=0)
                    except Rating.DoesNotExist:
                        Rating.objects.create(user=user, route=route, calification=0, recommendation=recommendation, date=BikeMeUtils.getCurrentDateString())
                        continue

                    rating.recommendation = recommendation 
                    rating.date = BikeMeUtils.getCurrentDateString()
                    rating.save()
                    