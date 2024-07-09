# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TournamentViewSet, TournamentDetailViewSet

router = DefaultRouter()
router.register(r'tournaments', TournamentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('tournaments/<int:detail_id>', TournamentViewSet.as_view({'get':'retrieve'}), name='tournament'),
    path('tournaments/<int:detail_id>/details', TournamentDetailViewSet.as_view({'get': 'retrieve'}), name="tournament_details")
]
