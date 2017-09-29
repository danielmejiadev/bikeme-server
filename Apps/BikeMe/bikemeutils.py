from django.utils import timezone

class BikeMeUtils():


	def getCurrentDate():
 	   return timezone.localtime(timezone.now())

	def getCurrentDateString():
 	   return timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')

