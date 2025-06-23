from rest_framework import serializers
from .models import Route, Point, BackgroundImage

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['id', 'x', 'y', 'order', 'created_at']

class RouteSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    background_url = serializers.CharField(source='background.image.url', read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'name', 'background_url', 'created_at', 'points']