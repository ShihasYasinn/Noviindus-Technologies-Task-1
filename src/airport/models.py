from django.db import models


class Airport(models.Model):
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.code


class AirportRoute(models.Model):
    POSITION_CHOICES = (
        ('LEFT', 'Left'),
        ('RIGHT', 'Right'),
    )

    parent = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='outgoing_routes'
    )
    child = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='incoming_routes'
    )
    position = models.CharField(max_length=5, choices=POSITION_CHOICES)
    duration = models.PositiveIntegerField()

    class Meta:
        unique_together = ('parent', 'position')

    def __str__(self):
        return f"{self.parent} -> {self.child} ({self.position})"


class AirportClosure(models.Model):
    ancestor = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='ancestor_links'
    )
    descendant = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='descendant_links'
    )
    depth = models.PositiveIntegerField()

    # Direction-aware path: L, R, LL, LR, RL, RR
    path = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = ('ancestor', 'descendant')
        indexes = [
            models.Index(fields=['ancestor', 'path']),
        ]

    def __str__(self):
        return f"{self.ancestor} -> {self.descendant} ({self.path})"
