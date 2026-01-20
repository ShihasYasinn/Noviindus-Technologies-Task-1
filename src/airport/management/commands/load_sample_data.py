from django.core.management.base import BaseCommand
from airport.models import Airport, AirportRoute
from airport.services import add_airport_route


class Command(BaseCommand):
    help = 'Load sample airport data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample airport data...')
        
        # Clear existing data
        AirportRoute.objects.all().delete()
        Airport.objects.all().delete()
        
        # Create sample airports
        airports_data = [
            'JFK',  # New York
            'LAX',  # Los Angeles
            'ORD',  # Chicago
            'DFW',  # Dallas
            'DEN',  # Denver
            'ATL',  # Atlanta
            'SFO',  # San Francisco
            'SEA',  # Seattle
            'MIA',  # Miami
            'BOS',  # Boston
            'LAS',  # Las Vegas
            'PHX',  # Phoenix
        ]
        
        airports = {}
        for code in airports_data:
            airport = Airport.objects.create(code=code)
            airports[code] = airport
            self.stdout.write(f'Created airport: {code}')
        
        # Create sample routes to build a tree structure
        routes_data = [
            # Root: JFK (New York as main hub)
            ('JFK', 'LAX', 'LEFT', 300),   # JFK -> LAX (5 hours)
            ('JFK', 'ORD', 'RIGHT', 150),  # JFK -> ORD (2.5 hours)
            
            # LAX branches
            ('LAX', 'SFO', 'LEFT', 90),    # LAX -> SFO (1.5 hours)
            ('LAX', 'DEN', 'RIGHT', 120),  # LAX -> DEN (2 hours)
            
            # ORD branches
            ('ORD', 'DFW', 'LEFT', 180),   # ORD -> DFW (3 hours)
            ('ORD', 'ATL', 'RIGHT', 120),  # ORD -> ATL (2 hours)
            
            # SFO branches
            ('SFO', 'SEA', 'LEFT', 120),   # SFO -> SEA (2 hours)
            ('SFO', 'LAS', 'RIGHT', 90),   # SFO -> LAS (1.5 hours)
            
            # DEN branches (longest route for testing)
            ('DEN', 'PHX', 'LEFT', 90),    # DEN -> PHX (1.5 hours)
            ('DEN', 'MIA', 'RIGHT', 420),  # DEN -> MIA (7 hours) - LONGEST ROUTE
            
            # DFW branches
            ('DFW', 'BOS', 'LEFT', 210),   # DFW -> BOS (3.5 hours)
            
            # ATL branches
            ('ATL', 'MIA', 'LEFT', 90),    # ATL -> MIA (1.5 hours)
        ]
        
        self.stdout.write('\nCreating routes...')
        for parent_code, child_code, position, duration in routes_data:
            parent = airports[parent_code]
            child = airports[child_code]
            
            try:
                add_airport_route(parent, child, position, duration)
                self.stdout.write(
                    f'Created route: {parent_code} -> {child_code} '
                    f'({position}, {duration} min)'
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error creating route {parent_code} -> {child_code}: {e}'
                    )
                )
        
        # Display summary
        total_airports = Airport.objects.count()
        total_routes = AirportRoute.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSample data loaded successfully!'
            )
        )
        self.stdout.write(f'Total airports: {total_airports}')
        self.stdout.write(f'Total routes: {total_routes}')
        
        # Show tree structure
        self.stdout.write('\n' + '='*50)
        self.stdout.write('AIRPORT TREE STRUCTURE:')
        self.stdout.write('='*50)
        self.stdout.write('''
JFK (Root Hub)
├── LEFT: LAX (300 min)
│   ├── LEFT: SFO (90 min)
│   │   ├── LEFT: SEA (120 min)
│   │   └── RIGHT: LAS (90 min)
│   └── RIGHT: DEN (120 min)
│       ├── LEFT: PHX (90 min)
│       └── RIGHT: MIA (420 min) ← LONGEST ROUTE
└── RIGHT: ORD (150 min)
    ├── LEFT: DFW (180 min)
    │   └── LEFT: BOS (210 min)
    └── RIGHT: ATL (120 min)
        └── LEFT: MIA (90 min)
        ''')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('TESTING SCENARIOS:')
        self.stdout.write('='*50)
        self.stdout.write('''
1. Longest Route: DEN -> MIA (420 minutes)
2. Find 2nd Left Node from JFK: SFO (path: LL)
3. Find 1st Right Node from LAX: DEN (path: R)
4. Find 3rd Left Node from JFK: SEA (path: LLL)
        ''')