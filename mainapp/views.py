from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from models import TempSaveForm, Object, Custom, Activity, AttributeAssignment, InitialTempSaveForm
from django.views.decorators.csrf import csrf_protect
from datetime import datetime as dt
import ast
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
objct = []

@csrf_protect
@login_required
#def InitialTempSave(request, objct=objct):
 #  if request.method == 'POST':
#	form = InitialTempSaveForm(request.POST)
 #       if form.is_valid():
  #         objct.append(form.cleaned_data['obj'])
   #     return HttpResponseRedirect('init/')
    #else: 
     #   form = InitialTempSaveForm()
      #  return render(request, 'form.html', {'form': form})

@csrf_protect
@login_required         
#def TempSave(request, objct=objct):
    #try: 
	#obj = objct[0]
    #except IndexError:
     #   obj = Object()
    #initial = {'name': obj.name_title, 'collection': obj.collection, 'author': obj.author, 'amount': obj.amount, 'is_fragment': obj.is_fragment,'size': obj.size_number, 'description': obj.description, 'condition': obj.condition, 'price': obj.price, 'material': obj.material, 'note': obj.note, 'technique': obj.technique, 'storage': obj.place, 'transferred_from': obj.transferred_from,  'transferred_to': obj.transferred_to, 'term_back': obj.term_back, 'aim_of_receiving': obj.aim_of_receiving_gen, 'way_of_found': obj.way_of_found, 'code': obj.identifier} 
def TempSave(request, objct=objct):
    if request.method == 'POST':
        form = TempSaveForm(request.POST, initial=initial)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Getting on temporary storage', actor=request.user)
            act.save()
            obj.name_title=cd['name']
            obj.collection=cd['collection']
            obj.is_fragment=cd['is_fragment']
            obj.amount=cd['amount']
            obj.material=cd['material']
            #obj.size_type=cd['size_type']
            #obj.size_number=ast.literal_eval(cd['size'][0:-1].split(':')[0])
            #obj.size_measurement_unit=ast.literal_eval(cd['size'][0:-1].split(':')[1])
            obj.size_number=cd['size']
            obj.author=cd['author']
            obj.description=cd['description']
            #obj.condition_descr=cd['condition_descr']
            obj.condition=cd['condition']
            obj.price=cd['price']
            obj.note=cd['note']
            obj.technique=cd['technique']
            obj.place=cd['storage']
            obj.transferred_from=cd['transferred_from']
            obj.transferred_to=cd['transferred_to']
            obj.term_back=cd['term_back']
            obj.aim_of_receiving_gen=cd['aim_of_receiving']
            obj.way_of_found=cd['way_of_found']
            obj.identifier=cd['code']
            obj.save()
            for (k, v) in cd.items():
                attr_assign=AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=obj)
                attr_assign.save()
            return HttpResponse('ok')
        return HttpResponse('ne ok')
    else:
	#form = TempSaveForm(initial = initial)
	form = TempSaveForm()
    	return render(request, 'form.html', {'form': form})


