from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, MenuViewSet, VoteViewSet, TodayResultsView

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'menus', MenuViewSet)

urlpatterns = [
    path('results/today/', TodayResultsView.as_view()),
    path('', include(router.urls)),
]
