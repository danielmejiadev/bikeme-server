from __future__ import absolute_import 
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from Apps.BikeMe.models.recommender_model import WeigthedSlopeOne
from Apps.BikeMe.models.clustering_model import KMedoids
 
logger = get_task_logger(__name__)
 
#A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(minute=0, hour=0, day_of_week="wednesday,sunday")))
def executeRecommender():
    weightedSlopeOne = WeigthedSlopeOne()
    weightedSlopeOne.execute()

@periodic_task(run_every=(crontab(minute=0, hour=0, day_of_week="tuesday,saturday")))
def executeCreationEvents():    
    kMedoids = KMedoids()
    kMedoids.run()
