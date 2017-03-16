from django.db import models

class Route(models.Model):
    name 						= models.CharField(max_length=50)
    description 		= models.TextField()
    distance 				= models.IntegerField()
    level  					= models.IntegerField()
    average_ratings = models.DecimalField(max_digits=3, decimal_places=2)
    created_at 			= models.DateTimeField(auto_now_add=True)
    updated_at 			= models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)


class User(models.Model):
    name      	= models.CharField(max_length=50)
    last_name 	= models.CharField(max_length=50)
    level 			= models.IntegerField()
    email 			= models.EmailField(unique=True)
    password 		= models.CharField(max_length=100)
    routes 			= models.ManyToManyField(Route, through='Rating', related_name='users')
    created_at 	= models.DateTimeField(auto_now_add=True)
    updated_at 	= models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)

        
class Rating(models.Model):
    user 					= models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    route 				= models.ForeignKey(Route, on_delete=models.CASCADE, related_name='ratings')
    calification 	= models.DecimalField(max_digits=3, decimal_places=2)
    recomendation	= models.DecimalField(max_digits=3, decimal_places=2)
    created_at 		= models.DateTimeField(auto_now_add=True)
    updated_at 		= models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)









