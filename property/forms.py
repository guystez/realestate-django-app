from unicodedata import name
from django import forms

class SearchingForm(forms.Form):
   room = forms.IntegerField(label='room')
   floor = forms.IntegerField(label='floor')
   property_type = forms.CharField(label='property_type ')
   square_meter = forms.IntegerField(label='square_meter')
   location = forms.CharField(label='location')
   street=forms.CharField(label='street')
   price= forms.IntegerField(label='price')
   investment_range = forms.IntegerField(label='investment_range')
   fields = '__all__'


   def __str__(self):
      return self.room +","+ self.floor+","+ self.property_type+","+ self.square_meter+","+ self.location+","+ self.street+","+ self.price+","+self.investment_range
   def __repr__(self):
         return self.__str__() 

   def get_form(self):
      return self.data.get('room'), self.data.get('floor'),self.data.get('property_type'),self.data.get('square_meter'),self.data.get('location'),self.data.get('street'),self.data.get('price'),self.data.get('investment_range')
      
