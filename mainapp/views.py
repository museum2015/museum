from django.shortcuts import render, HttpResponse
from models import TempSaveForm, Object, Custom, Activity, AttributeAssignment
from django.views.decorators.csrf import csrf_protect
from datetime import datetime as dt
import ast
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
@csrf_protect
#@login_required
def TempSave(request):
    form = TempSaveForm()
    if request.method == 'POST':
        form = TempSaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Getting on temporary storage', actor=request.user)
            act.save()
            obj = Object()
            obj.name_title=cd['name']
            obj.collection=cd['collection']
            obj.is_fragment=cd['is_fragment']
            obj.amount=cd['amount']
            obj.material=cd['material']
            obj.size_type=cd['size_type']
            obj.size_number=ast.literal_eval(cd['size'][0:-1].split(':')[0])
            obj.size_measurement_unit=ast.literal_eval(cd['size'][0:-1].split(':')[1])
            obj.author=cd['author']

            obj.save()
            for (k, v) in cd.items():
                attr_assign=AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=obj)
                attr_assign.save()
        else:
            form = TempSaveForm()
    return render(request, 'form.html', {'form': form})


