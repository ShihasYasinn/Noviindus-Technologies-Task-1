from django import forms
from airport.models import Airport


class AirportForm(forms.Form):
    code = forms.CharField(
        max_length=10,
        label="Airport Code",
        help_text="Enter a unique airport code (e.g., JFK, LAX, ORD)",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., JFK',
            'style': 'text-transform: uppercase;'
        })
    )

    def clean_code(self):
        code = self.cleaned_data['code'].upper()
        if Airport.objects.filter(code=code).exists():
            raise forms.ValidationError(f"Airport with code '{code}' already exists.")
        return code


class AirportRouteForm(forms.Form):
    parent = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="Parent Airport",
        help_text="Select the source/parent airport"
    )
    child = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="Child Airport", 
        help_text="Select the destination/child airport"
    )
    position = forms.ChoiceField(
        choices=[('LEFT', 'Left'), ('RIGHT', 'Right')],
        label="Tree Position",
        help_text="Choose the position in the tree structure"
    )
    duration = forms.IntegerField(
        min_value=1,
        label="Flight Duration (minutes)",
        help_text="Enter the flight duration in minutes"
    )


class NthNodeSearchForm(forms.Form):
    airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="Starting Airport",
        help_text="Select the airport to start searching from"
    )
    direction = forms.ChoiceField(
        choices=[('LEFT', 'Left'), ('RIGHT', 'Right')],
        label="Search Direction",
        help_text="Choose whether to search left or right in the tree"
    )
    n = forms.IntegerField(
        min_value=1,
        label="Node Position (N)",
        help_text="Enter the position number (1st, 2nd, 3rd, etc.)"
    )


class LongestRouteSearchForm(forms.Form):
    search_type = forms.ChoiceField(
        choices=[
            ('all', 'Find Longest Route in Entire System'),
            ('from_airport', 'Find Longest Route from Specific Airport'),
        ],
        label="Search Type",
        help_text="Choose how you want to search for the longest route",
        widget=forms.RadioSelect
    )
    airport = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="Starting Airport",
        help_text="Select the airport to find longest route from (only for specific airport search)",
        required=False
    )


class ShortestRouteSearchForm(forms.Form):
    source = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="Source Airport",
        help_text="Select the departure airport"
    )
    destination = forms.ModelChoiceField(
        queryset=Airport.objects.all(),
        label="Destination Airport", 
        help_text="Select the arrival airport"
    )
