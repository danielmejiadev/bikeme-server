from Apps.BikeMe.models.route_model import *
from Apps.BikeMe.models.user_model import *
from Apps.BikeMe.models.rating_model import *
from Apps.BikeMe.models.event_model import *
from Apps.BikeMe.models.guest_model import *
from django.db.models import Q
import math
from math import sqrt
import random
import numpy as np
import json
import datetime
from Apps.BikeMe.bikemeutils import BikeMeUtils

class KMedoids():

    def __init__(self):
        self.minUsersForCluster = 3
        self.weightRatingsDistance = 0.6
        self.weightLevelDistance = 0.4

        self.ratingsMatrix = {}
        self.users = []
        self.distancesMatrix = []

        self.kClusters = 0

        self.initUsersRatings()

        self.initalWords = ['Evento','Salida', 'Aventura', 'Recorrido', 'Excursión', 'Expedición', 'Viaje', 'Travesía', 'Jornada','Trayecto', 
                    'Paseo','Etapa', 'Ruta', 'Cicloruta', 'Ciclovía','Circuito']
 
        self.level = "nivel"
        self.complementWords  = {
            0:["%s novato" % (self.level),    "%s basico" % (self.level),     "%s principiante" % (self.level),"%s humano" % (self.level),   'facil',                      'simple', 'posible'],
            1:["%s aprendiz" % (self.level),  'elemental',                    'de transición'], 
            2:["%s intermedio" % (self.level),"%s medio" % (self.level),      "%s deportista" % (self.level),  'exigente'],
            3:["%s experto" % (self.level),   "%s profesional" % (self.level),'difícil',                       "%s espartano" % (self.level), "%s avanzado" % (self.level)],
            4:["%s maestro " % (self.level),  "%s Dios " % (self.level),      'imposible',                     'muy difícil',                 "%s superior" % (self.level), "%s piernas de hierro" % (self.level)]
        }
    
    def initUsersRatings(self):
        self.usersQuerySet = User.objects.all()
        for user in self.usersQuerySet:
            ratingsUser = {}
            for rating in user.ratings.filter(calification__gt=0, recommendation=0):
                ratingsUser[str(rating.route_id)] = rating.calification
            
            self.ratingsMatrix[str(user.uid)] = ratingsUser
            self.users.append([
                str(user.uid),
                user.level,
                user.preferenceDays,
                user.preferenceHours])

    def ratingsDistance(self, ratingsUser1, ratingsUser2):
        ''' Pearson distance between two n-dimensional set of ratings normalizate for values between [0,1] '''
        
        # Get the list of mutually rated items
        commonRatings={}
        for rating in ratingsUser1:
            if rating in ratingsUser2: 
                commonRatings[rating]=1
        
        # Find the number of elements
        n=len(commonRatings)
        
        # if they are no ratings in common, return 0
        if n==0: 
            return 0

        # Add up all the preferences
        sum1=sum([ratingsUser1[rating] for rating in commonRatings])
        sum2=sum([ratingsUser2[rating] for rating in commonRatings])
        
        # Sum up the squares
        sum1Sq=sum([pow(ratingsUser1[rating],2) for rating in commonRatings])
        sum2Sq=sum([pow(ratingsUser2[rating],2) for rating in commonRatings])
        
        # Sum up the products
        pSum=sum([ratingsUser1[rating]*ratingsUser2[rating] for rating in commonRatings])
        
        # Calculate Pearson score
        num=pSum-(sum1*sum2/n)
        den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))

        if den==0: 
            return 0
        
        pearsonCorrelation=num/den
        
        #Pearson correlation return values [-1,1], Normalize to values [0,1]
        return 1.0-self.normalization(pearsonCorrelation,-1.0,1.0,0,1.0)

    def levelDistance(self,point1, point2):
        #Level distancia take values [0,4], Normalize to values [0,1]
        return self.normalization(abs(point1-point2), 0, 4, 0, 1)

    def normalization(self, value,valueMin,valueMax,betweenMin,betweenMax):
        return ((betweenMax-betweenMin) * ((value-valueMin)/(valueMax-valueMin)) )+betweenMin

    def calculateDistancesMatrix(self, users, ratingsMatrix, weightRatingsDistance, weightLevelDistance):
        distancesMatrix = []
        for user1 in users:
            distancesVector = []
            for user2 in  users:
                distanceRatings = self.ratingsDistance(ratingsMatrix[user1[0]], ratingsMatrix[user2[0]])*weightRatingsDistance
                distanceLevel = self.levelDistance(user1[1],user2[1])*weightLevelDistance
                distancesVector.append(distanceRatings+distanceLevel)
            
            distancesMatrix.append(distancesVector)

        return distancesMatrix

    def calculateClusters(self,distancesMatrix,kClusters,maxIterations=1000):

        # determine dimensions of distance matrix distancesMatrix
        m, n = distancesMatrix.shape

        # randomly initialize an array of kClusters medoid indices
        medoidsList = np.arange(n)
        np.random.shuffle(medoidsList)
        medoidsList = np.sort(medoidsList[:kClusters])

        # create a copy of the array of medoid indices
        medoidsNew = np.copy(medoidsList)

        # initialize a dictionary to represent clusters
        clusters = {}

        for iteration in range(maxIterations):
            # determine clusters, i. e. arrays of data indices
            J = np.argmin(distancesMatrix[:,medoidsList], axis=1)
            for numCluster in range(kClusters):
                clusters[numCluster] = np.where(J==numCluster)[0]
            
            # update cluster medoidsList
            for numCluster in range(kClusters):
                cluster = clusters[numCluster]
                if(len(cluster)>0):
                    J = np.mean(distancesMatrix[np.ix_(cluster,cluster)],axis=1)
                    j = np.argmin(J)
                    medoidsNew[numCluster] = clusters[numCluster][j]
            
            np.sort(medoidsNew)

            # check for convergence
            if np.array_equal(medoidsList, medoidsNew):
                break
            medoidsList = np.copy(medoidsNew)
        
        else:
            # final update of cluster memberships
            J = np.argmin(distancesMatrix[:,medoidsList], axis=1)
            for numCluster in range(kClusters):
                clusters[numCluster] = np.where(J==numCluster)[0]


        # return results
        return medoidsList, clusters

    def reCalculateClusters(self, medoidsList, clusters, clustersToDelete, usersToLocate, distancesMatrix):
        medoidsDict = {}
        for k in clusters:
                medoidsDict[k]=medoidsList[k]
            
        for k in clustersToDelete:
            del medoidsDict[k]
            del clusters[k]

        for userToLocate in usersToLocate:
            closerMedoid = -1
            closerDistance = 1000
            for k in medoidsDict:
                distance = distancesMatrix[userToLocate][medoidsDict[k]]
                if(distance < closerDistance):
                    closerMedoid = k

            if(closerMedoid != -1):
                clusters[closerMedoid] = np.append(clusters[closerMedoid],userToLocate)

        return medoidsDict, clusters

    def calculateLevelClusters(self,clusters,users):
        levelClusters = {}
        p = 0.50
        for kCluster, clusterUsers in clusters.items():
            summ = 0
            for userIndex in clusterUsers:
                summ += users[userIndex][1]

            x = random.random()
            if x < p:
                levelClusters[kCluster] = math.floor(summ / len(clusterUsers))
            else:
                levelClusters[kCluster] = math.ceil(summ / len(clusterUsers))

        return levelClusters

    def generateEventName(self, level):
        initialWordIndex = random.randint(0,len(self.initalWords)-1)
        initialWord = self.initalWords[initialWordIndex]

        complementWordIndex = random.randint(0,len(self.complementWords[level])-1)
        complementWord = self.complementWords[level][complementWordIndex]
        return '%s %s' % (initialWord,complementWord)

    def calculateEventDate(self, cluster, users):

        def nextWeekDay(nextWeekDay):
            # 0 = Monday, 1=Tuesday, 2=Wednesday... 6=Sunday.
            today = BikeMeUtils.getCurrentDate()
            days_ahead = nextWeekDay - today.weekday()
            if days_ahead <= 0: # Target day already happened this week
                days_ahead += 7
            return today + datetime.timedelta(days_ahead)

        preferecesDaysCount = [0]*7
        preferecesHoursCount = [0]*3
        for userIndex in cluster:
            userPreferenceDays = json.loads(users[userIndex][2])
            userPreferenceHours = json.loads(users[userIndex][3])
            for preferDay in userPreferenceDays:
                preferecesDaysCount[preferDay] +=1

            for preferHour in userPreferenceHours:
                preferecesHoursCount[preferHour] +=1

        maximumDay = max(preferecesDaysCount)
        maximumHour = max(preferecesHoursCount)

        if(maximumDay/len(cluster) >= 0.50):
            maximumIndexDay = preferecesDaysCount.index(maximumDay)
        else:
            maximumIndexDay = random.randint(0,6)

        if(maximumHour/len(cluster) >= 0.50):
            maximumIndexHour = preferecesHoursCount.index(maximumHour)
        else:
            maximumIndexHour = random.randint(0,2)

        dateEvent = nextWeekDay(maximumIndexDay)

        if(maximumIndexHour==0):
            hourEvent = random.randint(7,12)
        elif(maximumIndexHour==1):
            hourEvent = random.randint(13,16)
        elif(maximumIndexHour==2):
            hourEvent = random.randint(7,16)

        dateEvent = dateEvent.replace(hour=hourEvent, minute=00)

        return dateEvent

    def createEvents(self, clusters, levelClusters, users):
        for kCluster in clusters:
            routesLevel = []
            levelExtend = 0
            levelCluster = levelClusters[kCluster]
            while not routesLevel:
                routes = list(Route.objects.filter( Q(level=levelCluster+levelExtend) | Q(level=levelCluster-levelExtend) ))
                routesLevel.extend(routes)
               
                if(levelExtend>= 4):
                    break
                else:
                    levelExtend+=1
            
            if routesLevel:
                routeIndex = random.randint(0, len(routesLevel)-1)
                routeEvent = routesLevel[routeIndex]
                eventName  = self.generateEventName(routeEvent.level)
                eventDate  = self.calculateEventDate(clusters[kCluster],users)
                event      = Event(name=eventName,route=routeEvent,date=eventDate)
                event.save()
                for userIndex in clusters[kCluster]:
                    user = self.usersQuerySet.get(pk=users[userIndex][0])
                    guest = Guest(user=user,event=event,date=BikeMeUtils.getCurrentDateString())
                    guest.save()

    def run(self): 
        numberUsers = len(self.users)
        if(numberUsers >= self.minUsersForCluster):

            self.kClusters = math.floor(numberUsers/self.minUsersForCluster)
            self.distancesMatrix = np.array(self.calculateDistancesMatrix(self.users, self.ratingsMatrix, self.weightRatingsDistance, self.weightLevelDistance))
            
            medoidsList, clusters = self.calculateClusters(self.distancesMatrix, self.kClusters)

            clustersToDelete = []
            usersToLocate = np.int_([])

            for k in clusters:
                if(len(clusters[k])<self.minUsersForCluster):
                    clustersToDelete.append(k)
                    usersToLocate = np.append(usersToLocate,clusters[k])

            if clustersToDelete:
                medoidsDict, clusters = self.reCalculateClusters(medoidsList, clusters, clustersToDelete, usersToLocate, self.distancesMatrix)
                
            levelClusters = self.calculateLevelClusters(clusters, self.users)
            self.createEvents(clusters, levelClusters, self.users)
