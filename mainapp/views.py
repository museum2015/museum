from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from models import TempSaveForm, Object, Custom, Activity, AttributeAssignment, InitialTempSaveForm ,TempRetForm
from django.views.decorators.csrf import csrf_protect
from datetime import datetime as dt
import ast
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

@csrf_protect
@login_required
def TempSave(request):
    if request.method == 'POST':
        form = TempSaveForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            act = Activity(time_stamp=dt.now(), type='Getting on temporary storage', actor=request.user)
            act.save()
            obj = Object()
            obj.save()
            for (k, v) in cd.items():
                attr_assign=AttributeAssignment(attr_name=k, attr_value=v, event_initiator=act, aim=obj)
                attr_assign.save()
            return HttpResponse('ok')
        return HttpResponse('ne ok')
    else:
        form = TempSaveForm()
    return render(request, 'AddOnTs.html', {'form': form})


@csrf_protect
def TempRet(request):
    form = TempRetForm()
    return request(request, 'ReturnFromTS.html', {'form': form})

def GetProject(request):
    act_list = Activity.objects.filter(approval=False)
    qs_list = []
    return render(request, 'projects.html', {'acts': act_list})

def ApproveProject(request, offset):
    Activity.objects.get(id=int(offset)).approve()
    return HttpResponse('Succesfully approved')