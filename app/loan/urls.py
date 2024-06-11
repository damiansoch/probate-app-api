"""
URL mapping for loan_application Api
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from loan import views

router = DefaultRouter()
router.register('solicitors', views.SolicitorViewSet, basename='solicitor')
router.register('agencies', views.AgencyViewSet, basename='agency')
router.register('applications', views.ApplicationViewSet, basename='application')
router.register('estates', views.EstateViewSet, basename='estate')
router.register('assets', views.AssetViewSet, basename='asset')
router.register('expenses', views.ExpenseViewSet, basename='expense')
router.register('disputes', views.DisputeViewSet, basename='dispute')

app_name = 'loan'

urlpatterns = [
    path('', include(router.urls)),
]
