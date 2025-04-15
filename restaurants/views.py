from datetime import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Restaurant, Menu, Vote
from .serializers import RestaurantSerializer, MenuSerializer, VoteSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='menu/(?P<date>\d{4}-\d{2}-\d{2})')
    def menu_by_date(self, request, pk=None, date=None):
        try:
            target_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'detail': 'Invalid date format use YYYY-MM-DD'}, status=400)

        restaurant = self.get_object()
        menu = restaurant.menus.filter(date=target_date).first()

        if not menu:
            return Response({'detail': f'No menu found for {date}'}, status=400)

        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='menus')
    def all_menus(self, request, pk=None):
        restaurant = self.get_object()
        menus = restaurant.menus.all()

        if not menus.exists():
            return Response({'detail': f'No menus found for {restaurant.name}'}, status=404)

        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='menu/today')
    def today_menu(self, request, pk=None):
        restaurant = self.get_object()
        today = datetime.today().date()
        menu = restaurant.menus.filter(date=today).first()

        if not menu:
            return Response({'detail': 'No menu for today.'}, status=404)

        serializer = MenuSerializer(menu)
        return Response(serializer.data)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        restaurant = serializer.validated_data['restaurant']
        serializer.save(restaurant=restaurant)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]


class TodayResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = datetime.today().date()
        restaurants = Restaurant.objects.all()
        data = []

        for restaurant in restaurants:
            vote_count = restaurant.votes.filter(date=today).count()
            data.append({
                'restaurant': restaurant.name,
                'votes': vote_count,
            })

        return Response(data)

