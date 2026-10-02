from django.db import models
from django.contrib.auth.models import User


# 👤 USER PROFILE (Role-based system)
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('donor', 'Donor'),
        ('volunteer', 'Volunteer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


# 🍱 FOOD POST
class FoodPost(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    expiry_time = models.DateTimeField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='Available')

    def __str__(self):
        return self.food_name


# 🙋 REQUEST SYSTEM
class Request(models.Model):
    STATUS_CHOICES = (
        ('Requested', 'Requested'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    food_post = models.ForeignKey(FoodPost, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Requested')

    def __str__(self):
        return f"{self.volunteer.username} → {self.food_post.food_name}"


# 🚚 PICKUP SYSTEM
class Pickup(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Picked', 'Picked'),
        ('Delivered', 'Delivered'),
    )

    request = models.OneToOneField(Request, on_delete=models.CASCADE)
    pickup_time = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.request.food_post.food_name} - {self.delivery_status}"