from django.urls import path
from airport.views import (
    home_view,
    add_airport_view,
    add_route_view,
    nth_node_view,
    longest_route_view,
    shortest_route_view
)

urlpatterns = [
    path('', home_view, name='home'),
    path('add-airport/', add_airport_view, name='add-airport'),
    path('add-route/', add_route_view, name='add-route'),
    path('nth-node/', nth_node_view, name='nth-node'),
    path('longest/', longest_route_view, name='longest-route'),
    path('shortest/', shortest_route_view, name='shortest-route'),
]
