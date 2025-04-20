from django.contrib.gis.db import models
from django.contrib.auth.models import User


class UserLocation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='locations')
    point = models.PointField(srid=4326)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.user.username} at {self.timestamp}"
    

    class Meta:
        ordering = ['-timestamp']

        

