from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from .models import Route, Point
from .serializers import RouteSerializer, PointSerializer
from django.db.models import Max


class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class PointViewSet(viewsets.ModelViewSet):
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Point.objects.filter(
            route__pk=self.kwargs['route_pk'],
            route__user=self.request.user
        ).order_by('order')

    def perform_create(self, serializer):
        route = get_object_or_404(Route, pk=self.kwargs['route_pk'], user=self.request.user)
        last = route.points.aggregate(max_order=Max('order'))['max_order'] or 0
        serializer.save(route=route, order=last + 1)