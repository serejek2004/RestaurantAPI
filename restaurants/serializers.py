from rest_framework import serializers
from .models import Restaurant, Menu, Vote
import datetime


class MenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'items', 'date']

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address']

    def create(self, validated_data):
        return Restaurant.objects.create(**validated_data)


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['restaurant']

    def validate_restaurant(self, value):
        today = datetime.date.today()

        if not Menu.objects.filter(restaurant=value, date=today).exists():
            raise serializers.ValidationError("This restaurant have not menu today.")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        today = datetime.date.today()

        if Vote.objects.filter(user=user, date=today).exists():
            raise serializers.ValidationError("You vote today.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return Vote.objects.create(user=user, date=datetime.date.today(), **validated_data)
