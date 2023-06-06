from django.db import models
from django.conf import settings

class ProcedureCategory(models.Model):
    CATEGORY_TYPE = (
        (1, "Процедуры"),
        (2, "Салоны"),
    )
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='images')
    category_type = models.IntegerField(choices=CATEGORY_TYPE)

    def __str__(self):
        return self.title

class Procedure(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images')
    description = models.TextField()
    category = models.ForeignKey(ProcedureCategory, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    duration = models.IntegerField()
    limit = models.IntegerField()

    def __str__(self):
        return self.title 

class ImageProcedure(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images')

    def __str__(self):
        return self.procedure.title 

class ServiceProcedure(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Schedule(models.Model):
    date = models.DateField()
    time = models.TimeField()
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    places_left = models.IntegerField()
    


class ProcedureLimit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    limit = models.IntegerField()

class Record(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_canceled = models.BooleanField(default=False)

class FavoriteProcedure(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.title

class Customer(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    


