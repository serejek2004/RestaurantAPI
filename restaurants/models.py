import datetime
from django.db import models
from django.conf import settings


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_current_menu(self):
        today = datetime.date.today()
        return self.menus.filter(date=today).first()

    def get_vote_count(self, date=None):
        if date is None:
            date = datetime.date.today()
        return self.votes.filter(date=date).count()


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
    date = models.DateField()
    items = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("restaurant", "date")

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="votes")
    date = models.DateField(default=datetime.date.today)

    class Meta:
        unique_together = ("user", "date")

    def __str__(self):
        return f"{self.user} voted for {self.restaurant.name} on {self.date}"
