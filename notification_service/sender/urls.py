from django.urls import path
from .views import (create_client, read_client,
                    update_client, delete_client,
                    create_mailing, update_mailing,
                    delete_mailing, read_mailing)


urlpatterns = [
    path('create_client/', create_client, name='create_client'),
    path('read_clients/', read_client, name='read_clients'),
    path('read_client/<int:id>', read_client, name='read_client'),
    path('update_client/<int:id>', update_client, name='update_client'),
    path('delete_client/<int:id>', delete_client, name='delete_client'),
    path('create_mailing/', create_mailing, name='create_mailing'),
    path('update_mailing/<int:id>', update_mailing, name='update_mailing'),
    path('delete_mailing/<int:id>', delete_mailing, name='delete_mailing'),
    path('read_mailings/', read_mailing, name='read_mailings'),
    path('read_mailing/<int:id>', read_mailing, name='read_mailing'),
]
