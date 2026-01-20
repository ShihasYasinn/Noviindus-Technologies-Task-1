from .models import AirportClosure, AirportRoute


def find_nth_left_node(airport, n):
    path = 'L' * n
    return (
        AirportClosure.objects
        .filter(ancestor=airport, path=path)
        .select_related('descendant')
        .first()
    )


def find_nth_right_node(airport, n):
    path = 'R' * n
    return (
        AirportClosure.objects
        .filter(ancestor=airport, path=path)
        .select_related('descendant')
        .first()
    )


def longest_route():
    return (
        AirportRoute.objects
        .select_related('parent', 'child')
        .order_by('-duration')
        .first()
    )


def longest_route_from_airport(airport):
    return (
        AirportRoute.objects
        .filter(parent=airport)
        .select_related('parent', 'child')
        .order_by('-duration')
        .first()
    )


def shortest_route_between(source, destination):
    return (
        AirportRoute.objects
        .filter(parent=source, child=destination)
        .order_by('duration')
        .first()
    )
