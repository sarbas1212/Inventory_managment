from django.urls import path
from .views import OutstandingReportAPIView, SalesReportAPIView, StockReportAPIView

urlpatterns = [
    path("sales/", SalesReportAPIView.as_view(), name="sales-report"),
    path("outstanding/", OutstandingReportAPIView.as_view()),
    path("stock/", StockReportAPIView.as_view()),
]
