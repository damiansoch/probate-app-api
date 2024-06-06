"""
URL mapping for loan_application Api
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from loan import views

router = DefaultRouter()
router.register('solicitors', views.SolicitorViewSet, basename='solicitor')

app_name = 'loan'

urlpatterns = [
    path('', include(router.urls)),
]
