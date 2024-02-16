
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=10)
    age = models.IntegerField(validators=[MinValueValidator(1)],default=1)
    def __str__(self): return f"{self.name}, Level: {self.level}, Age: {self.age}"

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room')
    name = models.CharField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability')
    day = models.CharField(max_length=10, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.user.name}'s availability on {self.day} from {self.start_time} to {self.end_time}"
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username} on {self.timestamp}"
class Tcourt(models.Model):
    name = models.CharField(max_length=200)
    image= models.ImageField(upload_to='base/tcourts/')
    wpage=models.CharField(max_length=200, default="")
    adress = models.CharField(max_length=200, default="")
    def __str__(self):
        return f"{self.name} - {self.image}"