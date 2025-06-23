from django import forms
from .models import Route, Point, GameBoard

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name']
        
class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ['x', 'y']
        widgets = {
            'x': forms.NumberInput(attrs={'id': 'id_x', 'step': 'any'}),
            'y': forms.NumberInput(attrs={'id': 'id_y', 'step': 'any'}),
        }
        
        
class GameBoardForm(forms.ModelForm):
    class Meta:
        model = GameBoard
        fields = ['name', 'rows', 'cols']