from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserApplicationList.as_view(), name="application_list"),
    path("active", views.ApplicationActiveList.as_view(), name="application_active_list"),
    path("cancel", views.ApplicationCancel.as_view(), name="application_cancel"),
    path("loan", views.ApplicationLoan.as_view(), name="application_loan"),
    path("payment", views.ApplicationPayment.as_view(), name="application_payment"),
    path("<int:pk>", views.ApplicationDetail.as_view(), name="application_detail"),
    path("<int:pk>/approve", views.ApplicationApprove.as_view(), name="application_approve"),
    path("<int:pk>/decline", views.ApplicationDecline.as_view(), name="application_decline"),
]
