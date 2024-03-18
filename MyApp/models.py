from django.db import models

# Create your models here.

class Color(models.Model):
    color_name = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self) -> str:
        return self.color_name
    
class Person(models.Model):
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="color", verbose_name = "color")
    name = models.CharField(max_length=255, blank=False)
    age = models.IntegerField()
    
    def __str__(self) -> str:
        return self.name


    