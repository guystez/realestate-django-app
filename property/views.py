from lib2to3.pgen2.token import GREATEREQUAL
from math import floor
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from library.settings import LOGIN_REDIRECT_URL
from django.contrib import messages
from property.models import Project, Property
from property.register import NewUserForm
from .forms import SearchingForm
from django.contrib.auth import login
# def list(request):
#    return HttpResponse("Hello DJANGO library")

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchingForm()

    return render(request, 'result.html', {'form': form})

 
def result(request):
    my_search = request.POST.get('searchproperty')
    new_form = SearchingForm(request.POST, request.FILES)
    new_form= new_form.get_form()
    found_apt = Property.objects.filter(room__lte = new_form[0],floor__lte = new_form[1],property_type__contains = new_form[2],square_meter__lte = new_form[3],location__contains = new_form[4],street__contains = new_form[5],price__lte = new_form[6],investment_range__lte = new_form[7]).values()
    final_price = []

    for apt in found_apt:
        apt_price=apt['price']
        # found_project = Project.objects.filter(location__contains = apt['location'],street__contains = apt['street'],street_number__range = apt['street_number']-15,).values()
        found_project = Project.objects.filter(street__contains= apt['street']).values()
        investment_range=new_form[7]
        for proj in found_project:
            our_date = proj['dates']-2022
            if new_form[7]>= our_date:

                new_price = apt_price*proj['value']
                apt_price = apt_price+new_price
            
                final_price.append(apt_price)
                
            
            

    context = {
        
        'final_price' : final_price,
        'apt':found_apt,

        'apt_price' : apt_price,
        
        'found_project' : found_project,
        'found_apt' : apt['location'],
        'room' : new_form[0],
        'floor' : new_form[1],
        'property_type' : new_form[2],
        'square_meter' : new_form[3],
        'location' : new_form[4],
        'street' : new_form[5],
        'price' : new_form[6]

    }

    return render(request,'result.html',context = context)


@login_required
def home(request):
    
#    template = loader.get_template('index.html')
   context = {
       'book_list': ['Harry Potter','Lord of the Rings','Hobbit'],
       'books':"books",
   }
  
   return render(request,'index.html',context)





def searchproperty(request):
   my_search = request.GET.get('searchproperty') 
   my_property = Property.objects.all()
   searchingform = SearchingForm(request.POST, request.FILES)
   context = ({
            'searchingform' : searchingform
            
           
        })
   return render(request,'searchproperty.html', context = context)  






def get_form(request):

    if request.method == 'POST':
        form = SearchingForm(request.POST)
        if form.is_valid():
            context = {
            'room' : form.cleaned_data['room'],
            'floor' : form.cleaned_data['floor'],
            'property_type' : form.cleaned_data['property_type'],
            'square_meter' : form.cleaned_data['square_meter'],
            'location' : form.cleaned_data['location'],
            'street' : form.cleaned_data['street'],
            'street_number' : form.cleaned_data['street_number'],
            'price' : form.cleaned_data['price']
            }
            
          

            return HttpResponseRedirect('/result',  context_instance=RequestContext(request))
    else:
        form = SearchingForm()
        rendered_form = form.render("searchproperty.html")
        context = {'form': rendered_form}
        
        return render(request, 'property/result.html', context)



def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("login.html")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

