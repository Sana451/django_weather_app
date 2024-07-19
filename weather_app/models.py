from django.db import models


class City(models.Model):
    title = models.CharField(primary_key=True, max_length=30)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def increment_count(self):
        self.count += 1
