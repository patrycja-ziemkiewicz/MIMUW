from django.db import models
from django.contrib.auth.models import User
from django.forms import JSONField

class BackgroundImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='backgrounds/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Route(models.Model):
    name = models.CharField(max_length=100, default='Nowa trasa')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routes')
    background = models.ForeignKey(
        'BackgroundImage', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='routes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Point(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='points')
    x = models.FloatField()
    y = models.FloatField()
    order = models.PositiveIntegerField('Kolejność na trasie', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Point {self.order} ({self.route.name})"
    
class GameBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    cols = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class Dot(models.Model):
    board = models.ForeignKey(GameBoard, on_delete=models.CASCADE, related_name='dots')
    row = models.PositiveIntegerField()
    col = models.PositiveIntegerField()
    color = models.CharField(max_length=7)
    
    class Meta:
        unique_together = ('board', 'row', 'col')

    def __str__(self):
        return f"Dot {self.color}@({self.row},{self.col}) on {self.board.title}"
    
class GamePath(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_paths')
    board = models.ForeignKey(GameBoard, on_delete=models.CASCADE, related_name='game_paths')
    data = models.JSONField(help_text="Obiekt: { 'hsl(0,100%,50%)': [ {'row':1,'col':2}, ... ], ... }")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'board')

    def __str__(self):
        return f"Path by {self.user} on {self.board}"
