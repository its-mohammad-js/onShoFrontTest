from django.urls import path
from . import views

urlpatterns = [
    path('ordersub', views.OrderCreateView.as_view(), name='user-profile-order'),
    path('userorders', views.UserOrdersView.as_view(), name='user-orders'),
    path('complete', views.PaymentCompleteView.as_view(), name='payment-complete'),
    path('gateway/init', views.PaymentGatewayInitView.as_view(), name='payment-gateway-init'),
    path('callback', views.PaymentCallbackView.as_view(), name='payment-callback'),
    # Purchase Code endpoints
    path('code/create', views.OrganizationPurchaseCodeCreateView.as_view(), name='create-purchase-code'),
    path('code/list', views.OrganizationPurchaseCodeListView.as_view(), name='list-purchase-codes'),
    path('code/redeem', views.CodeRedeemView.as_view(), name='redeem-code'),
    path('code/redemptions', views.UserCodeRedemptionsListView.as_view(), name='user-code-redemptions'),
    path('courses', views.CourseListView.as_view(), name='list-courses'),
]
