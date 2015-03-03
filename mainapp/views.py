from django.shortcuts import render, HttpResponse
from models import TempSaveForm, Object, Custom, Activity, AttributeAssignment
from django.views.decorators.csrf import csrf_protect
from datetime import datetime as dt
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
            #...and so on...
            obj.save()
            for (k, v) in cd.items():
                attr_assign=AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=obj)
                attr_assign.save()
        else:
            form = TempSaveForm()
    return render(request, 'form.html', {'form': form})


