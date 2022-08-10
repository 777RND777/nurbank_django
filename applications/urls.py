from django.urls import path

from .views import *

urlpatterns = [
    path("", UserApplicationListView.as_view(), name="application_list"),
    path("active", ApplicationActiveListView.as_view(), name="application_active_list"),
    path("cancel", ApplicationCancelView.as_view(), name="application_cancel"),
    path("loan", ApplicationLoanView.as_view(), name="application_loan"),
    path("payment", ApplicationPaymentView.as_view(), name="application_payment"),
    path("<int:pk>", ApplicationDetailView.as_view(), name="application"),
    path("<int:pk>/approve", ApplicationApproveView.as_view(), name="application_approve"),
    path("<int:pk>/decline", ApplicationDeclineView.as_view(), name="application_decline"),
]
