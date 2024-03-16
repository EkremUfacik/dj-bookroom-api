from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    max_occupancy = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} - {self.max_occupancy}"
    
class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    attendees = models.IntegerField()
    
    def __str__(self):
        return f"{self.room.name} - {self.start_time} - {self.end_time}"
    
    
