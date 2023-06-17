from django.urls import path

from base.user.views import signup_user, login_user, logout_user, home
from base.batch.views import batches, batch, create_batch, update_batch,\
    delete_batch, mortality, create_mortality, update_mortality, delete_mortality
from base.item.views import store_items, create_item, update_item, delete_item, forward_item
from base.sale.views import sale, make_sale, update_sale, delete_sale

urlpatterns = [
    path('', home, name='home-url'),

    path('signup/', signup_user, name='signup-url'),
    path('login/', login_user, name='login-url'),
    path('logout/', logout_user, name='logout-url'),

    path('batches/', batches, name='batches-url'),
    path('batches/<str:pk>/', batch, name='batch-url'),
    path('create-batch/', create_batch, name='create-batch-url'),
    path('update-batch/<str:pk>/', update_batch, name='update-batch-url'),
    path('delete-batch/<str:pk>/', delete_batch, name='delete-batch-url'),

    path('store/', store_items, name='store-url'),
    path('create-item/', create_item, name='create-item-url'),
    path('update-item/<str:pk>/', update_item, name='update-item-url'),
    path('delete-item/<str:pk>/', delete_item, name='delete-item-url'),
    path('forwared-item/<str:pk>/', forward_item, name='forward-item-url'),

    path('sales/', sale, name='sales-url'),
    path('make-sale/', make_sale, name='make-sale-url'),
    path('update-sale/<str:pk>', update_sale, name='update-sale-url'),
    path('delete-sale/<str:pk>', delete_sale, name='delete-sale-url'),

    path('mortalities/', mortality, name='mortalities-url'),
    path('create-mortality/', create_mortality, name='create-mortality-url'),
    path('update-mortality/<str:pk>', update_mortality, name='update-mortality-url'),
    path('delete-mortality/<str:pk>', delete_mortality, name='delete-mortality-url'),
]