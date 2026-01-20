from django.db import transaction
from .models import AirportRoute, AirportClosure


@transaction.atomic
def add_airport_route(parent, child, position, duration):
    # 1. Create direct route
    AirportRoute.objects.create(
        parent=parent,
        child=child,
        position=position,
        duration=duration
    )

    # 2. Self reference for child
    AirportClosure.objects.get_or_create(
        ancestor=child,
        descendant=child,
        depth=0,
        path=''
    )

    direction = 'L' if position == 'LEFT' else 'R'

    # 3. Copy all ancestor paths of parent
    parent_closures = AirportClosure.objects.filter(descendant=parent)

    bulk = []
    for row in parent_closures:
        bulk.append(
            AirportClosure(
                ancestor=row.ancestor,
                descendant=child,
                depth=row.depth + 1,
                path=row.path + direction
            )
        )

    AirportClosure.objects.bulk_create(bulk)
