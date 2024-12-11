from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"excel-basic", ExcelBasicController, basename='excel-basic')

urlpatterns = [
    path('', include(router.urls)),
    path('request-create-info',
         ExcelBasicController.as_view({ 'get': 'requestCreateExcelInfo' }),
         name='excel 정보 데이터 생성'),
    # path('request-create-info',
    #      ExcelBasicController.as_view({ 'get': 'requestDatabaseToExcel' }),
    #      name='DB 데이터를 excel로 생성'),
]