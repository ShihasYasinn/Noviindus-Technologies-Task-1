from django.shortcuts import render, redirect
from django.contrib import messages
from airport.forms import AirportForm, AirportRouteForm, NthNodeSearchForm, LongestRouteSearchForm, ShortestRouteSearchForm
from airport.services import add_airport_route
from airport.queries import (
    find_nth_left_node,
    find_nth_right_node,
    longest_route,
    longest_route_from_airport,
    shortest_route_between
)
from airport.models import Airport, AirportRoute


#--------------------HOME PAGE------------------------------

def home_view(request):
    # Get some basic statistics for the dashboard
    total_airports = Airport.objects.count()
    total_routes = AirportRoute.objects.count()
    longest_route_info = longest_route()
    
    context = {
        'total_airports': total_airports,
        'total_routes': total_routes,
        'longest_route': longest_route_info,
    }
    return render(request, 'airport/home.html', context)



#--------------------ADD AIRPORT------------------------------

def add_airport_view(request):
    form = AirportForm(request.POST or None)

    if form.is_valid():
        Airport.objects.create(code=form.cleaned_data['code'])
        messages.success(request, f"Airport '{form.cleaned_data['code']}' added successfully!")
        return redirect('add-airport')

    # Get current airports for display
    airports_list = Airport.objects.all().order_by('code')
    airports_count = airports_list.count()

    return render(request, 'airport/add_airport.html', {
        'form': form,
        'airports_list': airports_list,
        'airports_count': airports_count
    })


#--------------------ADD ROUTE------------------------------

def add_route_view(request):
    # Check if there are airports available
    if Airport.objects.count() < 2:
        messages.warning(request, "You need at least 2 airports to create a route. Please add airports first.")
        return redirect('add-airport')
    
    form = AirportRouteForm(request.POST or None)

    if form.is_valid():
        try:
            add_airport_route(
                parent=form.cleaned_data['parent'],
                child=form.cleaned_data['child'],
                position=form.cleaned_data['position'],
                duration=form.cleaned_data['duration']
            )
            messages.success(request, f"Route from {form.cleaned_data['parent'].code} to {form.cleaned_data['child'].code} added successfully!")
            return redirect('add-route')
        except Exception as e:
            messages.error(request, f"Error adding route: {str(e)}")

    return render(request, 'airport/add_route.html', {'form': form})



#-------------------Nth Node (Requirement 1)----------------------------------

def nth_node_view(request):
    form = NthNodeSearchForm(request.POST or None)
    result = None
    search_performed = False

    if form.is_valid():
        search_performed = True
        airport = form.cleaned_data['airport']
        n = form.cleaned_data['n']
        direction = form.cleaned_data['direction']

        if direction == 'LEFT':
            result = find_nth_left_node(airport, n)
        else:
            result = find_nth_right_node(airport, n)

    return render(request, 'airport/nth_node.html', {
        'form': form,
        'result': result.descendant if result else None,
        'search_performed': search_performed,
        'search_details': {
            'airport': form.cleaned_data.get('airport') if form.is_valid() else None,
            'direction': form.cleaned_data.get('direction') if form.is_valid() else None,
            'n': form.cleaned_data.get('n') if form.is_valid() else None,
        } if form.is_valid() else None
    })


#------------------Longest Route (Requirement 2)-------------------------------

def longest_route_view(request):
    form = LongestRouteSearchForm(request.POST or None)
    route = None
    search_performed = False
    search_type = None

    if form.is_valid():
        search_performed = True
        search_type = form.cleaned_data['search_type']
        
        if search_type == 'all':
            route = longest_route()
        elif search_type == 'from_airport':
            airport = form.cleaned_data['airport']
            if airport:
                route = longest_route_from_airport(airport)
            else:
                form.add_error('airport', 'Please select an airport for specific airport search.')
                search_performed = False

    return render(request, 'airport/longest.html', {
        'form': form,
        'route': route,
        'search_performed': search_performed,
        'search_type': search_type,
        'search_details': {
            'search_type': form.cleaned_data.get('search_type') if form.is_valid() else None,
            'airport': form.cleaned_data.get('airport') if form.is_valid() else None,
        } if form.is_valid() else None
    })


#-------------------Shortest Route (Requirement 3)-----------------------------

def shortest_route_view(request):
    form = ShortestRouteSearchForm(request.POST or None)
    route = None
    search_performed = False

    if form.is_valid():
        search_performed = True
        source = form.cleaned_data['source']
        destination = form.cleaned_data['destination']
        route = shortest_route_between(source, destination)

    return render(request, 'airport/shortest.html', {
        'form': form,
        'route': route,
        'search_performed': search_performed,
        'search_details': {
            'source': form.cleaned_data.get('source') if form.is_valid() else None,
            'destination': form.cleaned_data.get('destination') if form.is_valid() else None,
        } if form.is_valid() else None
    })
